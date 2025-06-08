from __future__ import annotations

from config_parser import ConfigBase


class Config(ConfigBase):
    function_length_limit: int = 30
    model_name: str = "claude-3-7-sonnet-latest"
