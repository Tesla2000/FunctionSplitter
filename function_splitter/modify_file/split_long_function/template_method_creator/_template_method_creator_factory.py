from __future__ import annotations

from function_splitter._config import Config
from function_splitter.exceptions import NotAble2SplitException
from function_splitter.modify_file.split_long_function.template_method_creator._one_shot_creator._one_shot_creator import (
    OneShotCreator,
)
from libcst import FunctionDef
from libcst import Module

from ._overt_creator import OvertCreator
from ._step_by_step_creator import StepByStepCreator
from ._template_method_creator import TemplateMethodCreator


def template_method_creator_factory(
    function_def: FunctionDef, config: Config
) -> TemplateMethodCreator:
    function_code = Module([function_def]).code
    return StepByStepCreator(config, function_def, function_code)
    if len(function_code.splitlines()) <= config.oneshot_length_limit:
        return OneShotCreator(function_def, config.model_name)
    elif config.use_overt_creator:
        return OvertCreator(
            function_def, config.model_name, config.submethod_creation_step
        )
    else:
        raise NotAble2SplitException
    # elif config.
    # else:
    #     return StepByStepCreator(function_code, config.model_name)
