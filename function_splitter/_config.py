from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from config_parser import ConfigBase
from dotenv import load_dotenv
from pydantic import Field


class Config(ConfigBase):
    root: Path = Field(default_factory=lambda: Path(os.getcwd()))
    function_length_limit: int = 50
    oneshot_length_limit: int = Field(
        default=100,
        description="Upper limit of function length. Beyond certain value LLM response becomes unstable.",
    )
    use_overt_creator: bool = Field(
        default=False, description="Experimental and unstable method"
    )
    submethod_creation_step: int = 3
    max_iterations: int = 10
    model_name: str = "claude-3-7-sonnet-latest"
    env_path: str = Field(
        description="Path to env path",
        default=".env",
    )

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        os.chdir(self.root)
        load_dotenv(Path(os.getcwd()).joinpath(self.env_path))
