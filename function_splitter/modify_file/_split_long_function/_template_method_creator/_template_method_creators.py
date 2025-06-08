from __future__ import annotations

import json
from abc import ABC
from abc import abstractmethod
from typing import TypeVar

from _example import EXAMPLE
from _template_method import TemplateMethod
from _template_method import TemplateMethodConstructor
from _template_method import TemplateMethodMainMethod
from _template_method import TemplateMethodNameAndFields
from _template_method import TemplateMethodSubmethods
from litellm import completion
from pydantic import BaseModel

TemplateMethodComponent = TypeVar("TemplateMethodComponent", bound=BaseModel)


class _TemplateMethodCreator(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def create(self, function_code: str) -> TemplateMethod:
        pass

    def _create_component(
        self, prompt: str, component_class: type[TemplateMethodComponent]
    ) -> TemplateMethodComponent:
        model_response = completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
            response_format=component_class,
        )
        return component_class(
            **json.loads(model_response.choices[0]["message"].content)
        )


class _OneShotCreator(_TemplateMethodCreator):
    def create(self, function_code: str) -> TemplateMethod:
        return self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "\nWhen creating calls take into account if functions are asynchronous add await or async for if needed. "
                "\nFUNCTION:"
                f"\n{function_code}"
            ),
            TemplateMethod,
        )


class _StepByStepCreator(_TemplateMethodCreator):
    def __init__(self, model_name: str, example: str = EXAMPLE):
        super().__init__(model_name)
        self.example = example

    def create(self, function_code: str) -> TemplateMethod:
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
