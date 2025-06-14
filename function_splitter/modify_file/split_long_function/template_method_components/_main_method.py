from __future__ import annotations

from typing import Any

from libcst import Module
from libcst import Name
from pydantic import Field as PydanticField

from ._base_method_description import BASE_METHOD_DESCRIPTIONS
from ._method import Method


class MainMethod(Method):
    code: str = PydanticField(description=(BASE_METHOD_DESCRIPTIONS))

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.code = Module(
            [
                self._function_def.with_changes(
                    name=Name(self._function_def.name.value.lstrip("_"))
                )
            ]
        ).code
