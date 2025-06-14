from __future__ import annotations

from libcst import FunctionDef
from libcst import Module
from modify_file.split_long_function.template_method_components import (
    Constructor,
)

from ._constructor_fields_extractor import constructor_fields_extractor
from ._variable_name_replacer import VariableNameReplacer


def get_constructor_and_fields(
    function_node: FunctionDef,
) -> tuple[Constructor, set[str], str]:
    replacer = VariableNameReplacer(function_node)
    self_function_code = Module([function_node.visit(replacer)]).code
    self_names = replacer.replaced_names
    constructor_fields = constructor_fields_extractor(function_node)
    constructor = Constructor(fields=list(constructor_fields))
    return constructor, self_names, self_function_code
