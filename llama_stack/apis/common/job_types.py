# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
from enum import Enum

from pydantic import BaseModel

from llama_stack.schema_utils import json_schema_type


class JobStatus(Enum):
    completed = "completed"
    in_progress = "in_progress"
    failed = "failed"
    scheduled = "scheduled"


@json_schema_type
class Job(BaseModel):
    job_id: str
    status: JobStatus
