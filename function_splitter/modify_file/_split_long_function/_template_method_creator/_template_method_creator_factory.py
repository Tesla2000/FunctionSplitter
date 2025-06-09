from __future__ import annotations

from _config import Config
from libcst import FunctionDef
from libcst import Module

from ._one_shot_creator import OneShotCreator
from ._overt_creator import OvertCreator
from ._step_by_step_creator import StepByStepCreator
from ._template_method_creator import TemplateMethodCreator


def template_method_creator_factory(
    function_def: FunctionDef, config: Config
) -> TemplateMethodCreator:
    if config.user_overt_creator:
        return OvertCreator(function_def, config.model_name)
    function_code = Module([function_def]).code
    if len(function_code.splitlines()) <= config.oneshot_length_limit:
        return OneShotCreator(function_code, config.model_name)
    else:
        return StepByStepCreator(function_code, config.model_name)
