from __future__ import annotations

from config_parser import ConfigBase
from pydantic import Field


class Config(ConfigBase):
    function_length_limit: int = 30
    oneshot_length_limit: int = Field(
        default=100,
        description="Upper limit of function length. Beyond certain value LLM response becomes unstable.",
    )
    model_name: str = "claude-3-7-sonnet-latest"
