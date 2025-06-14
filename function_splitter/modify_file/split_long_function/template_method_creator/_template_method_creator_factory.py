from __future__ import annotations

from _config import Config
from exceptions import NotAble2SplitException
from libcst import FunctionDef
from libcst import Module
from modify_file.split_long_function.template_method_creator._one_shot_creator._one_shot_creator import (
    OneShotCreator,
)

from ._overt_creator import OvertCreator
from ._template_method_creator import TemplateMethodCreator


def template_method_creator_factory(
    function_def: FunctionDef, config: Config
) -> TemplateMethodCreator:
    function_code = Module([function_def]).code
    if len(function_code.splitlines()) <= config.oneshot_length_limit:
        return OneShotCreator(function_def, config.model_name)
    elif config.user_overt_creator:
        return OvertCreator(
            function_def, config.model_name, config.submethod_creation_step
        )
    else:
        raise NotAble2SplitException
    # elif config.
    # else:
    #     return StepByStepCreator(function_code, config.model_name)
