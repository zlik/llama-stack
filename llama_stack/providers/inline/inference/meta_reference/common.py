# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

from llama_stack.distribution.utils.model_utils import model_local_dir


class TokenResult(BaseModel):
    token: int
    text: str
    logprobs: Optional[List[float]] = None


def model_checkpoint_dir(model_id) -> str:
    checkpoint_dir = Path(model_local_dir(model_id))

    paths = [Path(checkpoint_dir / f"consolidated.{ext}") for ext in ["pth", "00.pth"]]
    if not any(p.exists() for p in paths):
        checkpoint_dir = checkpoint_dir / "original"

    assert checkpoint_dir.exists(), (
        f"Could not find checkpoints in: {model_local_dir(model_id)}. "
        f"If you try to use the native llama model, Please download model using `llama download --model-id {model_id}`"
        f"Otherwise, please save you model checkpoint under {model_local_dir(model_id)}"
    )
    return str(checkpoint_dir)
