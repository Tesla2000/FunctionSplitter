from __future__ import annotations

from function_splitter.modify_file.split_long_function.template_method_components import (
    TemplateMethod,
)
from function_splitter.modify_file.split_long_function.template_method_creator._get_constructor_and_fields import (
    get_constructor_and_fields,
)
from function_splitter.modify_file.split_long_function.template_method_creator._template_method_creator import (
    TemplateMethodCreator,
)
from libcst import FunctionDef

from ._missing_elements import _MissingElements


class OneShotCreator(TemplateMethodCreator):
    def __init__(self, function_def: FunctionDef, model_name: str):
        super().__init__(model_name)
        self.function_def = function_def

    def create(self) -> TemplateMethod:
        constructor, self_fields, self_function_code = (
            get_constructor_and_fields(self.function_def)
        )
        missing_elements = self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "\nWhen creating calls take into account if functions are asynchronous add await or async for if needed. "
                "\nFUNCTION:"
                f"\n{self_function_code}"
                "\n\nSELF FIELDS:\n" + "\n".join(self_fields)
            ),
            _MissingElements,
        )
        return TemplateMethod(
            constructor=constructor,
            main_method=missing_elements.main_method,
            submethods=missing_elements.submethods,
            fields=missing_elements.fields,
            name=missing_elements.class_name,
        )
