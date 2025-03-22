# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Any, Dict, Optional

from pydantic import BaseModel


class BingSearchToolConfig(BaseModel):
    """Configuration for Bing Search Tool Runtime"""

    api_key: Optional[str] = None
    top_k: int = 3

    @classmethod
    def sample_run_config(cls, __distro_dir__: str, **kwargs: Any) -> Dict[str, Any]:
        return {
            "api_key": "${env.BING_API_KEY:}",
        }
