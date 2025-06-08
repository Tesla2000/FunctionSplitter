from __future__ import annotations

from sys import path

path.insert(0, "/".join(__file__.split("/")[:-1]))

from _modify_file import modify_file

__all__ = ["modify_file"]
