# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from llama_stack.schema_utils import json_schema_type


@json_schema_type
class RunpodImplConfig(BaseModel):
    url: Optional[str] = Field(
        default=None,
        description="The URL for the Runpod model serving endpoint",
    )
    api_token: Optional[str] = Field(
        default=None,
        description="The API token",
    )

    @classmethod
    def sample_run_config(cls, **kwargs: Any) -> Dict[str, Any]:
        return {
            "url": "${env.RUNPOD_URL:}",
            "api_token": "${env.RUNPOD_API_TOKEN:}",
        }
