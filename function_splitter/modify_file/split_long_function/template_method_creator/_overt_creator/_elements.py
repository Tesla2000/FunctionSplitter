from __future__ import annotations

from typing import Any
from typing import Optional

from libcst import Attribute
from libcst import CSTVisitor
from libcst import FunctionDef
from libcst import Name
from modify_file.split_long_function.template_method_components import Field
from modify_file.split_long_function.template_method_components import (
    MainMethod,
)
from pydantic import BaseModel
from pydantic import Field as PydanticField


class FieldAny(Field):
    field_type: str = "Any"


class Submethod(BaseModel):
    start_line: int = PydanticField(
        description="Number of the line from the input function that should be the first line of the submethod"
    )
    end_line: int = PydanticField(
        description="Number of the line from the input function that should be the last line of the submethod (inclusive)"
    )
    function_name: str


class MissingElements(BaseModel):
    _field_and_method_names: list[str]
    main_method: MainMethod = PydanticField(description="Must be public")
    class_name: str

    def __init__(self, /, **data: Any):
        main_method = data["main_method"]
        if isinstance(main_method, str):
            data["main_method"] = MainMethod(code=main_method)
        super().__init__(**data)
        self._set_submethods()

    def _set_submethods(self):
        self._field_and_method_names = _submethod_names_getter(
            self.main_method.function_def
        )

    @property
    def field_and_method_names(self) -> list[str]:
        return self._field_and_method_names


def _submethod_names_getter(function_def: FunctionDef) -> list[str]:
    names = []

    class Visitor(CSTVisitor):
        def visit_Attribute(self, node: "Attribute") -> Optional[bool]:
            if (
                isinstance(node.value, Name)
                and node.value.value == "self"
                and node.attr.value not in names
            ):
                names.append(node.attr.value)
            return super().visit_Attribute(node)

    function_def.visit(Visitor())
    return names
