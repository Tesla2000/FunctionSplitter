from __future__ import annotations

import libcst
from _config import Config
from _convert_self2name import convert_self2name
from _template_method_creator import template_method_creator_factory
from libcst import ClassDef
from libcst import FunctionDef
from libcst import Module


def split_long_function(
    function_def: FunctionDef, module: Module, config: Config
) -> "ClassDef":
    function_def = convert_self2name(function_def, module)
    function_code = Module([function_def]).code
    template_method_creator = template_method_creator_factory(
        function_code, config
    )
    template_method = template_method_creator.create(function_code)
    class_def = libcst.parse_statement(
        str(template_method).replace("\t", 4 * " ")
    )
    assert isinstance(
        class_def, ClassDef
    ), f"{split_long_function.__name__} failed to produce {ClassDef.__name__}. Produced {type(class_def).__name__} instead"
    return class_def
