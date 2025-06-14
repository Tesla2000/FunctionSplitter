from __future__ import annotations

import libcst
from function_splitter._config import Config
from libcst import ClassDef
from libcst import FunctionDef
from libcst import Module

from ._convert_self2name import convert_self2name
from .template_method_creator import template_method_creator_factory


def split_long_function(
    function_def: FunctionDef, module: Module, config: Config
) -> "ClassDef":
    function_def = convert_self2name(function_def, module)
    template_method_creator = template_method_creator_factory(
        function_def, config
    )
    template_method = template_method_creator.create()
    class_def = libcst.parse_statement(
        str(template_method).replace("\t", 4 * " ")
    )
    assert isinstance(
        class_def, ClassDef
    ), f"{split_long_function.__name__} failed to produce {ClassDef.__name__}. Produced {type(class_def).__name__} instead"
    return class_def
