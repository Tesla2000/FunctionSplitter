from __future__ import annotations

from sys import path

from . import template_method_components as template_method_components
from ._split_long_function import split_long_function

path.insert(0, "/".join(__file__.split("/")[:-1]))

__all__ = [
    "split_long_function",
    "template_method_components",
]
