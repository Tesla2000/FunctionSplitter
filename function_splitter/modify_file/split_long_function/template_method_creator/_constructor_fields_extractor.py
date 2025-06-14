from __future__ import annotations

from libcst import Annotation
from libcst import FunctionDef
from libcst import Module
from modify_file.split_long_function.template_method_components import Field


def constructor_fields_extractor(
    function_def: FunctionDef,
) -> tuple[Field, ...]:
    return tuple(
        Field(
            field_name=param.name.value,
            field_type=(
                Module([annotation.annotation]).code
                if isinstance(annotation := param.annotation, Annotation)
                else None
            ),
        )
        for param in function_def.params.params
    )
