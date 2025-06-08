from __future__ import annotations

from sys import path

from _template_method_creator._template_method_creator_factory import (
    template_method_creator_factory,
)

path.insert(0, "/".join(__file__.split("/")[:-1]))

__all__ = ["template_method_creator_factory"]
