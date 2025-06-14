from __future__ import annotations

from sys import path

from .main import main

path.insert(0, "/".join(__file__.split("/")[:-1]))

__all__ = ["main"]
