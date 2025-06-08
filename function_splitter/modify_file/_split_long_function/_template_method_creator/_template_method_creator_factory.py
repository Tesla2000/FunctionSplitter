from __future__ import annotations

from _config import Config
from _template_method_creators import _OneShotCreator
from _template_method_creators import _StepByStepCreator
from _template_method_creators import _TemplateMethodCreator


def template_method_creator_factory(
    function_code: str, config: Config
) -> _TemplateMethodCreator:
    if len(function_code.splitlines()) <= config.oneshot_length_limit:
        return _OneShotCreator(config.model_name)
    else:
        return _StepByStepCreator(config.model_name)
