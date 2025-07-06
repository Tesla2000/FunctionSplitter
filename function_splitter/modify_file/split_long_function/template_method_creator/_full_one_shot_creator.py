from __future__ import annotations

from function_splitter.modify_file.split_long_function.template_method_components import (
    TemplateMethod,
)
from function_splitter.modify_file.split_long_function.template_method_creator._template_method_creator import (
    TemplateMethodCreator,
)


class FullOneShotCreator(TemplateMethodCreator):
    def __init__(self, function_code: str, model_name: str):
        super().__init__(model_name)
        self.function_code = function_code

    def create(self) -> TemplateMethod:
        response = self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "\nWhen creating calls take into account if functions are asynchronous add await or async for if needed. "
                "\nConstructor should contain the same parameters as the original function. "
                "\nFUNCTION:"
                f"\n{self.function_code}"
            ),
            TemplateMethod,
        )
        return response
