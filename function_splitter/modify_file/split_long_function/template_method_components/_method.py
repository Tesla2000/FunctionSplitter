from __future__ import annotations

from typing import Any

import libcst
from libcst import FunctionDef
from pydantic import BaseModel
from pydantic import Field as PydanticField

from ._base_method_description import BASE_METHOD_DESCRIPTIONS


class Method(BaseModel):
    code: str = PydanticField(
        description=(
            BASE_METHOD_DESCRIPTIONS
            + "Submethods should be mostly 2-4 lines long."
        )
    )
    _function_def: FunctionDef

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.code = self.code.removeprefix('<parameter name="code">')
        function_def = libcst.parse_statement(self.code)
        assert isinstance(function_def, FunctionDef)
        self._function_def = function_def

    @property
    def function_def(self) -> FunctionDef:
        return self._function_def

    def __str__(self):
        return "".join(map("\n\t".__add__, self.code.splitlines()))
