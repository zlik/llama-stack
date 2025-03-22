# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Protocol, Tuple

import pydantic

from llama_stack.distribution.datatypes import KVStoreConfig, RoutableObjectWithProvider
from llama_stack.distribution.utils.config_dirs import DISTRIBS_BASE_DIR
from llama_stack.log import get_logger
from llama_stack.providers.utils.kvstore import KVStore, kvstore_impl
from llama_stack.providers.utils.kvstore.config import SqliteKVStoreConfig

logger = get_logger(__name__, category="core")


class DistributionRegistry(Protocol):
    async def get_all(self) -> List[RoutableObjectWithProvider]: ...

    async def initialize(self) -> None: ...

    async def get(self, identifier: str) -> Optional[RoutableObjectWithProvider]: ...

    def get_cached(self, identifier: str) -> Optional[RoutableObjectWithProvider]: ...

    async def update(self, obj: RoutableObjectWithProvider) -> RoutableObjectWithProvider: ...

    async def register(self, obj: RoutableObjectWithProvider) -> bool: ...

    async def delete(self, type: str, identifier: str) -> None: ...


REGISTER_PREFIX = "distributions:registry"
KEY_VERSION = "v8"
KEY_FORMAT = f"{REGISTER_PREFIX}:{KEY_VERSION}::" + "{type}:{identifier}"


def _get_registry_key_range() -> Tuple[str, str]:
    """Returns the start and end keys for the registry range query."""
    start_key = f"{REGISTER_PREFIX}:{KEY_VERSION}"
    return start_key, f"{start_key}\xff"


def _parse_registry_values(values: List[str]) -> List[RoutableObjectWithProvider]:
    """Utility function to parse registry values into RoutableObjectWithProvider objects."""
    all_objects = []
    for value in values:
        try:
            obj = pydantic.TypeAdapter(RoutableObjectWithProvider).validate_json(value)
            all_objects.append(obj)
        except pydantic.ValidationError as e:
            logger.error(f"Error parsing registry value, raw value: {value}. Error: {e}")
            continue

    return all_objects


class DiskDistributionRegistry(DistributionRegistry):
    def __init__(self, kvstore: KVStore):
        self.kvstore = kvstore

    async def initialize(self) -> None:
        pass

    def get_cached(self, type: str, identifier: str) -> Optional[RoutableObjectWithProvider]:
        # Disk registry does not have a cache
        raise NotImplementedError("Disk registry does not have a cache")

    async def get_all(self) -> List[RoutableObjectWithProvider]:
        start_key, end_key = _get_registry_key_range()
        values = await self.kvstore.range(start_key, end_key)
        return _parse_registry_values(values)

    async def get(self, type: str, identifier: str) -> Optional[RoutableObjectWithProvider]:
        json_str = await self.kvstore.get(KEY_FORMAT.format(type=type, identifier=identifier))
        if not json_str:
            return None

        try:
            return pydantic.TypeAdapter(RoutableObjectWithProvider).validate_json(json_str)
        except pydantic.ValidationError as e:
            logger.error(f"Error parsing registry value for {type}:{identifier}, raw value: {json_str}. Error: {e}")
            return None

    async def update(self, obj: RoutableObjectWithProvider) -> None:
        await self.kvstore.set(
            KEY_FORMAT.format(type=obj.type, identifier=obj.identifier),
            obj.model_dump_json(),
        )
        return obj

    async def register(self, obj: RoutableObjectWithProvider) -> bool:
        existing_obj = await self.get(obj.type, obj.identifier)
        # dont register if the object's providerid already exists
        if existing_obj and existing_obj.provider_id == obj.provider_id:
            return False

        await self.kvstore.set(
            KEY_FORMAT.format(type=obj.type, identifier=obj.identifier),
            obj.model_dump_json(),
        )
        return True

    async def delete(self, type: str, identifier: str) -> None:
        await self.kvstore.delete(KEY_FORMAT.format(type=type, identifier=identifier))


class CachedDiskDistributionRegistry(DiskDistributionRegistry):
    def __init__(self, kvstore: KVStore):
        super().__init__(kvstore)
        self.cache: Dict[Tuple[str, str], RoutableObjectWithProvider] = {}
        self._initialized = False
        self._initialize_lock = asyncio.Lock()
        self._cache_lock = asyncio.Lock()

    @asynccontextmanager
    async def _locked_cache(self):
        """Context manager for safely accessing the cache with a lock."""
        async with self._cache_lock:
            yield self.cache

    async def _ensure_initialized(self):
        """Ensures the registry is initialized before operations."""
        if self._initialized:
            return

        async with self._initialize_lock:
            if self._initialized:
                return

            start_key, end_key = _get_registry_key_range()
            values = await self.kvstore.range(start_key, end_key)
            objects = _parse_registry_values(values)

            async with self._locked_cache() as cache:
                for obj in objects:
                    cache_key = (obj.type, obj.identifier)
                    cache[cache_key] = obj

            self._initialized = True

    async def initialize(self) -> None:
        await self._ensure_initialized()

    def get_cached(self, type: str, identifier: str) -> Optional[RoutableObjectWithProvider]:
        return self.cache.get((type, identifier), None)

    async def get_all(self) -> List[RoutableObjectWithProvider]:
        await self._ensure_initialized()
        async with self._locked_cache() as cache:
            return list(cache.values())

    async def get(self, type: str, identifier: str) -> Optional[RoutableObjectWithProvider]:
        await self._ensure_initialized()
        cache_key = (type, identifier)

        async with self._locked_cache() as cache:
            return cache.get(cache_key, None)

    async def register(self, obj: RoutableObjectWithProvider) -> bool:
        await self._ensure_initialized()
        success = await super().register(obj)

        if success:
            cache_key = (obj.type, obj.identifier)
            async with self._locked_cache() as cache:
                cache[cache_key] = obj

        return success

    async def update(self, obj: RoutableObjectWithProvider) -> None:
        await super().update(obj)
        cache_key = (obj.type, obj.identifier)
        async with self._locked_cache() as cache:
            cache[cache_key] = obj
        return obj

    async def delete(self, type: str, identifier: str) -> None:
        await super().delete(type, identifier)
        cache_key = (type, identifier)
        async with self._locked_cache() as cache:
            if cache_key in cache:
                del cache[cache_key]


async def create_dist_registry(
    metadata_store: Optional[KVStoreConfig],
    image_name: str,
) -> tuple[CachedDiskDistributionRegistry, KVStore]:
    # instantiate kvstore for storing and retrieving distribution metadata
    if metadata_store:
        dist_kvstore = await kvstore_impl(metadata_store)
    else:
        dist_kvstore = await kvstore_impl(
            SqliteKVStoreConfig(db_path=(DISTRIBS_BASE_DIR / image_name / "kvstore.db").as_posix())
        )
    dist_registry = CachedDiskDistributionRegistry(dist_kvstore)
    await dist_registry.initialize()
    return dist_registry, dist_kvstore
