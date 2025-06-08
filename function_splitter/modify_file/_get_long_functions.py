from __future__ import annotations

from typing import Optional

import libcst
from _config import Config
from libcst import FunctionDef
from libcst import Module


def get_long_functions(module: Module, config: Config) -> set[FunctionDef]:
    functions = set()

    class LongFunctionDetector(libcst.CSTTransformer):
        def visit_FunctionDef(self, node: "FunctionDef") -> Optional[bool]:
            if (
                len(Module([node]).code.splitlines())
                > config.function_length_limit
            ):
                functions.add(node)
            return super().visit_FunctionDef(node)

    module.visit(LongFunctionDetector())
    return functions
