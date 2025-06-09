from __future__ import annotations

from _split_long_function._template_method import Field
from libcst import Annotation
from libcst import FunctionDef
from libcst import Module


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
