# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import asyncio
import contextvars
import logging
import queue
import random
import threading
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from llama_stack.apis.telemetry import (
    LogSeverity,
    Span,
    SpanEndPayload,
    SpanStartPayload,
    SpanStatus,
    StructuredLogEvent,
    Telemetry,
    UnstructuredLogEvent,
)
from llama_stack.log import get_logger
from llama_stack.providers.utils.telemetry.trace_protocol import serialize_value

logger = get_logger(__name__, category="core")


INVALID_SPAN_ID = 0x0000000000000000
INVALID_TRACE_ID = 0x00000000000000000000000000000000


def trace_id_to_str(trace_id: int) -> str:
    """Convenience trace ID formatting method
    Args:
        trace_id: Trace ID int

    Returns:
        The trace ID as 32-byte hexadecimal string
    """
    return format(trace_id, "032x")


def span_id_to_str(span_id: int) -> str:
    """Convenience span ID formatting method
    Args:
        span_id: Span ID int

    Returns:
        The span ID as 16-byte hexadecimal string
    """
    return format(span_id, "016x")


def generate_span_id() -> str:
    span_id = random.getrandbits(64)
    while span_id == INVALID_SPAN_ID:
        span_id = random.getrandbits(64)
    return span_id_to_str(span_id)


def generate_trace_id() -> str:
    trace_id = random.getrandbits(128)
    while trace_id == INVALID_TRACE_ID:
        trace_id = random.getrandbits(128)
    return trace_id_to_str(trace_id)


CURRENT_TRACE_CONTEXT = contextvars.ContextVar("trace_context", default=None)
BACKGROUND_LOGGER = None


class BackgroundLogger:
    def __init__(self, api: Telemetry, capacity: int = 1000):
        self.api = api
        self.log_queue = queue.Queue(maxsize=capacity)
        self.worker_thread = threading.Thread(target=self._process_logs, daemon=True)
        self.worker_thread.start()

    def log_event(self, event):
        try:
            self.log_queue.put_nowait(event)
        except queue.Full:
            logger.error("Log queue is full, dropping event")

    def _process_logs(self):
        while True:
            try:
                event = self.log_queue.get()
                # figure out how to use a thread's native loop
                asyncio.run(self.api.log_event(event))
            except Exception:
                import traceback

                traceback.print_exc()
                print("Error processing log event")
            finally:
                self.log_queue.task_done()

    def __del__(self):
        self.log_queue.join()


class TraceContext:
    spans: List[Span] = []

    def __init__(self, logger: BackgroundLogger, trace_id: str):
        self.logger = logger
        self.trace_id = trace_id

    def push_span(self, name: str, attributes: Dict[str, Any] = None) -> Span:
        current_span = self.get_current_span()
        span = Span(
            span_id=generate_span_id(),
            trace_id=self.trace_id,
            name=name,
            start_time=datetime.now(timezone.utc),
            parent_span_id=current_span.span_id if current_span else None,
            attributes=attributes,
        )

        self.logger.log_event(
            StructuredLogEvent(
                trace_id=span.trace_id,
                span_id=span.span_id,
                timestamp=span.start_time,
                attributes=span.attributes,
                payload=SpanStartPayload(
                    name=span.name,
                    parent_span_id=span.parent_span_id,
                ),
            )
        )

        self.spans.append(span)
        return span

    def pop_span(self, status: SpanStatus = SpanStatus.OK):
        span = self.spans.pop()
        if span is not None:
            self.logger.log_event(
                StructuredLogEvent(
                    trace_id=span.trace_id,
                    span_id=span.span_id,
                    timestamp=span.start_time,
                    attributes=span.attributes,
                    payload=SpanEndPayload(
                        status=status,
                    ),
                )
            )

    def get_current_span(self):
        return self.spans[-1] if self.spans else None


def setup_logger(api: Telemetry, level: int = logging.INFO):
    global BACKGROUND_LOGGER

    if BACKGROUND_LOGGER is None:
        BACKGROUND_LOGGER = BackgroundLogger(api)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(TelemetryHandler())


async def start_trace(name: str, attributes: Dict[str, Any] = None) -> TraceContext:
    global CURRENT_TRACE_CONTEXT, BACKGROUND_LOGGER

    if BACKGROUND_LOGGER is None:
        logger.debug("No Telemetry implementation set. Skipping trace initialization...")
        return

    trace_id = generate_trace_id()
    context = TraceContext(BACKGROUND_LOGGER, trace_id)
    context.push_span(name, {"__root__": True, **(attributes or {})})

    CURRENT_TRACE_CONTEXT.set(context)
    return context


async def end_trace(status: SpanStatus = SpanStatus.OK):
    global CURRENT_TRACE_CONTEXT

    context = CURRENT_TRACE_CONTEXT.get()
    if context is None:
        logger.debug("No trace context to end")
        return

    context.pop_span(status)
    CURRENT_TRACE_CONTEXT.set(None)


def severity(levelname: str) -> LogSeverity:
    if levelname == "DEBUG":
        return LogSeverity.DEBUG
    elif levelname == "INFO":
        return LogSeverity.INFO
    elif levelname == "WARNING":
        return LogSeverity.WARN
    elif levelname == "ERROR":
        return LogSeverity.ERROR
    elif levelname == "CRITICAL":
        return LogSeverity.CRITICAL
    else:
        raise ValueError(f"Unknown log level: {levelname}")


# TODO: ideally, the actual emitting should be done inside a separate daemon
# process completely isolated from the server
class TelemetryHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # horrendous hack to avoid logging from asyncio and getting into an infinite loop
        if record.module in ("asyncio", "selector_events"):
            return

        global CURRENT_TRACE_CONTEXT, BACKGROUND_LOGGER

        if BACKGROUND_LOGGER is None:
            raise RuntimeError("Telemetry API not initialized")

        context = CURRENT_TRACE_CONTEXT.get()
        if context is None:
            return

        span = context.get_current_span()
        if span is None:
            return

        BACKGROUND_LOGGER.log_event(
            UnstructuredLogEvent(
                trace_id=span.trace_id,
                span_id=span.span_id,
                timestamp=datetime.now(timezone.utc),
                message=self.format(record),
                severity=severity(record.levelname),
            )
        )

    def close(self):
        pass


class SpanContextManager:
    def __init__(self, name: str, attributes: Dict[str, Any] = None):
        self.name = name
        self.attributes = attributes
        self.span = None

    def __enter__(self):
        global CURRENT_TRACE_CONTEXT
        context = CURRENT_TRACE_CONTEXT.get()
        if not context:
            logger.debug("No trace context to push span")
            return self

        self.span = context.push_span(self.name, self.attributes)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global CURRENT_TRACE_CONTEXT
        context = CURRENT_TRACE_CONTEXT.get()
        if not context:
            logger.debug("No trace context to pop span")
            return

        context.pop_span()

    def set_attribute(self, key: str, value: Any):
        if self.span:
            if self.span.attributes is None:
                self.span.attributes = {}
            self.span.attributes[key] = serialize_value(value)

    async def __aenter__(self):
        global CURRENT_TRACE_CONTEXT
        context = CURRENT_TRACE_CONTEXT.get()
        if not context:
            logger.debug("No trace context to push span")
            return self

        self.span = context.push_span(self.name, self.attributes)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        global CURRENT_TRACE_CONTEXT
        context = CURRENT_TRACE_CONTEXT.get()
        if not context:
            logger.debug("No trace context to pop span")
            return

        context.pop_span()

    def __call__(self, func: Callable):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            async with self:
                return await func(*args, **kwargs)

        @wraps(func)
        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                return async_wrapper(*args, **kwargs)
            else:
                return sync_wrapper(*args, **kwargs)

        return wrapper


def span(name: str, attributes: Dict[str, Any] = None):
    return SpanContextManager(name, attributes)


def get_current_span() -> Optional[Span]:
    global CURRENT_TRACE_CONTEXT
    if CURRENT_TRACE_CONTEXT is None:
        logger.debug("No trace context to get current span")
        return None

    context = CURRENT_TRACE_CONTEXT.get()
    if context:
        return context.get_current_span()
    return None
