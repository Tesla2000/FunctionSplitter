from __future__ import annotations

from pathlib import Path

import libcst
from _config import Config
from exceptions import NotAble2SplitException
from libcst import ClassDef
from libcst import FunctionDef
from more_itertools.more import map_except
from pydantic import ValidationError

from ._function2template_method import function2template_method
from ._get_long_functions import get_long_functions
from .split_long_function import split_long_function


def modify_file(filepath: Path, config: Config) -> int:
    code = filepath.read_text()
    module = libcst.parse_module(code)
    long_functions = get_long_functions(module, config)
    replacements: dict["FunctionDef", "ClassDef"] = dict(
        map_except(
            lambda function: (
                function,
                split_long_function(function, module, config),
            ),
            long_functions,
            NotAble2SplitException,
            ValidationError,
        )
    )
    updated_module = function2template_method(replacements, module)
    new_code = updated_module.code
    if new_code != code:
        filepath.write_text(new_code)
        print(f"File {filepath} was modified")
        return 1
    return 0
