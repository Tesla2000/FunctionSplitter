from __future__ import annotations

from typing import NamedTuple

from function_splitter.modify_file.split_long_function.template_method_components import (
    Constructor,
)
from libcst import FunctionDef
from libcst import Module

from ._constructor_fields_extractor import constructor_fields_extractor
from ._variable_name_replacer import VariableNameReplacer


class _ConstructorInfo(NamedTuple):
    constructor: Constructor
    self_names: set[str]
    self_function_code: str


def get_constructor_and_fields(
    function_node: FunctionDef,
) -> _ConstructorInfo:
    replacer = VariableNameReplacer(function_node)
    self_function_code = Module([function_node.visit(replacer)]).code
    self_names = replacer.replaced_names
    constructor_fields = constructor_fields_extractor(function_node)
    constructor = Constructor(fields=list(constructor_fields))
    return _ConstructorInfo(constructor, self_names, self_function_code)
