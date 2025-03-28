# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import List

from llama_stack.models.llama.datatypes import CoreModelId
from llama_stack.providers.utils.inference.model_registry import (
    ProviderModelEntry,
    build_hf_repo_model_entry,
)

_MODEL_ENTRIES = [
    build_hf_repo_model_entry(
        "meta/llama-3.1-8b-instruct",
        CoreModelId.llama3_1_8b_instruct.value,
    )
]


def get_model_entries() -> List[ProviderModelEntry]:
    return _MODEL_ENTRIES
