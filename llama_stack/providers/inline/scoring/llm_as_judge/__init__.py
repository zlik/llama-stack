# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
from typing import Any, Dict

from llama_stack.distribution.datatypes import Api

from .config import LlmAsJudgeScoringConfig


async def get_provider_impl(
    config: LlmAsJudgeScoringConfig,
    deps: Dict[Api, Any],
):
    from .scoring import LlmAsJudgeScoringImpl

    impl = LlmAsJudgeScoringImpl(config, deps[Api.datasetio], deps[Api.datasets], deps[Api.inference])
    await impl.initialize()
    return impl
