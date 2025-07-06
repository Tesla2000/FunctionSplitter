from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from config_parser import ConfigBase
from pydantic import Field


class Config(ConfigBase):
    root: Path = Field(default_factory=lambda: Path(os.getcwd()))
    function_length_limit: int = Field(
        default=50,
        description="Functions below this length will not be taken into account",
    )
    oneshot_length_limit: int = Field(
        default=2137,
        description="Upper limit of function length. Beyond this value functions will be split with multistep method.",
    )
    multipart_length_limit: int = Field(
        default=sys.maxsize,
        description="Upper limit of function length. Beyond this value functions won't be split.",
    )
    use_overt_creator: bool = Field(
        default=False, description="Experimental and unstable method"
    )
    submethod_creation_step: int = 3
    max_iterations: int = 10
    model_name: str = "gpt-4.1"
    env_path: str = Field(
        description="Path to env path",
        default=".env",
    )

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        os.chdir(self.root)


if __name__ == "__main__":
    Config()
