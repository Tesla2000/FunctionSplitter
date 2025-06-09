from __future__ import annotations

from _split_long_function._template_method import TemplateMethod

from ._template_method_creator import TemplateMethodCreator


class OneShotCreator(TemplateMethodCreator):
    def __init__(self, function_code: str, model_name: str):
        super().__init__(model_name)
        self.function_code = function_code

    def create(self) -> TemplateMethod:
        return self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "\nWhen creating calls take into account if functions are asynchronous add await or async for if needed. "
                "\nFUNCTION:"
                f"\n{self.function_code}"
            ),
            TemplateMethod,
        )
