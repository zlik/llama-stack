# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from llama_stack.apis.common.type_system import NumberType
from llama_stack.apis.scoring_functions import (
    AggregationFunctionType,
    BasicScoringFnParams,
    ScoringFn,
)

ifeval = ScoringFn(
    identifier="basic::ifeval",
    description="Eval intruction follow capacity by checkping how many instructions can be followed in each example",
    return_type=NumberType(),
    provider_id="basic",
    provider_resource_id="ifeval",
    params=BasicScoringFnParams(
        aggregation_functions=[AggregationFunctionType.weighted_average],
    ),
)
