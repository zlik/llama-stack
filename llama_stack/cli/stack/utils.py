# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from enum import Enum


class ImageType(Enum):
    CONDA = "conda"
    CONTAINER = "container"
    VENV = "venv"


def print_subcommand_description(parser, subparsers):
    """Print descriptions of subcommands."""
    description_text = ""
    for name, subcommand in subparsers.choices.items():
        description = subcommand.description
        description_text += f"  {name:<21} {description}\n"
    parser.epilog = description_text
