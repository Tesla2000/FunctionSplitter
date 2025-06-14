from __future__ import annotations

from modify_file.split_long_function.template_method_components import (
    TemplateMethod,
)
from modify_file.split_long_function.template_method_components import (
    TemplateMethodConstructor,
)
from modify_file.split_long_function.template_method_components import (
    TemplateMethodMainMethod,
)
from modify_file.split_long_function.template_method_components import (
    TemplateMethodNameAndFields,
)
from modify_file.split_long_function.template_method_components import (
    TemplateMethodSubmethods,
)

from ._example import EXAMPLE
from ._template_method_creator import TemplateMethodCreator


class StepByStepCreator(TemplateMethodCreator):
    def __init__(
        self, model_name: str, function_code: str, example: str = EXAMPLE
    ):
        super().__init__(model_name)
        self.function_code = function_code
        self.example = example

    def create(self) -> TemplateMethod:
        function_code = self.function_code
        name_and_fields = self._create_name_and_fields(function_code)
        constructor = self._create_constructor(function_code, name_and_fields)
        submethods = self._create_submethods(
            function_code, name_and_fields, constructor
        )
        main_method = self._create_main_method(
            function_code, name_and_fields, constructor, submethods
        )
        return TemplateMethod(
            name=name_and_fields.name,
            fields=name_and_fields.fields,
            constructor=constructor.constructor,
            submethods=submethods.submethods,
            main_method=main_method.main_method,
        )

    def _create_name_and_fields(
        self, function_code: str
    ) -> TemplateMethodNameAndFields:
        return self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "In the first step create TemplateMethod name and create fields. "
                "\nFUNCTION:"
                f"\n{function_code}" + self.example
            ),
            TemplateMethodNameAndFields,
        )

    def _create_constructor(
        self, function_code: str, name_and_fields: TemplateMethodNameAndFields
    ) -> TemplateMethodConstructor:
        return self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "In this step create TemplateMethod constructor. "
                "\nFUNCTION:"
                f"\n{function_code}"
                "\n\nExtracted name and fields:"
                f"\n{name_and_fields}" + self.example
            ),
            TemplateMethodConstructor,
        )

    def _create_submethods(
        self,
        function_code: str,
        name_and_fields: TemplateMethodNameAndFields,
        constructor: TemplateMethodConstructor,
    ) -> TemplateMethodSubmethods:
        return self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "In this step create TemplateMethod submethods. "
                "\nFUNCTION:"
                f"\n{function_code}"
                "\n\nExtracted name and fields:"
                f"\n{name_and_fields}"
                "\n\nCreated constructor:"
                f"\n{constructor}" + self.example
            ),
            TemplateMethodSubmethods,
        )

    def _create_main_method(
        self,
        function_code: str,
        name_and_fields: TemplateMethodNameAndFields,
        constructor: TemplateMethodConstructor,
        submethods: TemplateMethodSubmethods,
    ) -> TemplateMethodMainMethod:
        return self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "In this step create TemplateMethod submethods. "
                "\nWhen creating calls take into account if functions are asynchronous add await or async for if needed. "
                "\nFUNCTION:"
                f"\n{function_code}"
                "\n\nExtracted name and fields:"
                f"\n{name_and_fields}"
                "\n\nCreated constructor:"
                f"\n{constructor}"
                "\n\nCreated submethods:"
                f"\n{submethods}" + self.example
            ),
            TemplateMethodMainMethod,
        )
