# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Any, Dict

from .config import LocalFSDatasetIOConfig


async def get_provider_impl(
    config: LocalFSDatasetIOConfig,
    _deps: Dict[str, Any],
):
    from .datasetio import LocalFSDatasetIOImpl

    impl = LocalFSDatasetIOImpl(config)
    await impl.initialize()
    return impl
