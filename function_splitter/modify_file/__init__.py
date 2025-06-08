from __future__ import annotations

from sys import path

from modify_file._modify_file import modify_file

path.insert(0, "/".join(__file__.split("/")[:-1]))

__all__ = ["modify_file"]
