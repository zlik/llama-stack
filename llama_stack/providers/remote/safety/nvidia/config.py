# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
import os
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from llama_stack.schema_utils import json_schema_type


@json_schema_type
class NVIDIASafetyConfig(BaseModel):
    """
    Configuration for the NVIDIA Guardrail microservice endpoint.

    Attributes:
        guardrails_service_url (str): A base url for accessing the NVIDIA guardrail endpoint, e.g. http://0.0.0.0:7331
        config_id (str): The ID of the guardrails configuration to use from the configuration store
         (https://developer.nvidia.com/docs/nemo-microservices/guardrails/source/guides/configuration-store-guide.html)

    """

    guardrails_service_url: str = Field(
        default_factory=lambda: os.getenv("GUARDRAILS_SERVICE_URL", "http://0.0.0.0:7331"),
        description="The url for accessing the guardrails service",
    )
    config_id: Optional[str] = Field(default="self-check", description="Config ID to use from the config store")

    @classmethod
    def sample_run_config(cls, **kwargs) -> Dict[str, Any]:
        return {
            "guardrails_service_url": "${env.GUARDRAILS_SERVICE_URL:http://localhost:7331}",
            "config_id": "self-check",
        }
