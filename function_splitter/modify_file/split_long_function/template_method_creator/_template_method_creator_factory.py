from __future__ import annotations

from function_splitter._config import Config
from function_splitter.exceptions import NotAble2SplitException
from libcst import FunctionDef
from libcst import Module

from ._full_one_shot_creator import FullOneShotCreator
from ._multistep_creator import MultistepCreator
from ._overt_creator import OvertCreator
from ._template_method_creator import TemplateMethodCreator


def template_method_creator_factory(
    function_def: FunctionDef, config: Config
) -> TemplateMethodCreator:
    function_code = Module([function_def]).code
    if config.use_overt_creator:
        return OvertCreator(
            function_def, config.model_name, config.submethod_creation_step
        )
    function_length = len(function_code.splitlines())
    if function_length <= config.oneshot_length_limit:
        return FullOneShotCreator(function_code, config.model_name)
    if function_length <= config.multipart_length_limit:
        raise ValueError(
            f"{MultistepCreator.__name__} still to be implemented"
        )  # TODO: Implement
        return MultistepCreator(function_def, config.model_name)
    else:
        raise NotAble2SplitException
