# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Optional

from pydantic import BaseModel, Field

from llama_stack.schema_utils import json_schema_type


@json_schema_type
class VLLMInferenceAdapterConfig(BaseModel):
    url: Optional[str] = Field(
        default=None,
        description="The URL for the vLLM model serving endpoint",
    )
    max_tokens: int = Field(
        default=4096,
        description="Maximum number of tokens to generate.",
    )
    api_token: Optional[str] = Field(
        default="fake",
        description="The API token",
    )
    tls_verify: bool = Field(
        default=True,
        description="Whether to verify TLS certificates",
    )

    @classmethod
    def sample_run_config(
        cls,
        url: str = "${env.VLLM_URL}",
        **kwargs,
    ):
        return {
            "url": url,
            "max_tokens": "${env.VLLM_MAX_TOKENS:4096}",
            "api_token": "${env.VLLM_API_TOKEN:fake}",
            "tls_verify": "${env.VLLM_TLS_VERIFY:true}",
        }
