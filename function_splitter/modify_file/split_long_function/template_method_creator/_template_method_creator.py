from __future__ import annotations

import json
from abc import ABC
from abc import abstractmethod
from typing import TypeVar

from function_splitter.modify_file.split_long_function.template_method_components import (
    TemplateMethod,
)
from pydantic import BaseModel

TemplateMethodComponent = TypeVar("TemplateMethodComponent", bound=BaseModel)


class _ComponentCreator(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def create_component(
        self, prompt: str, component_class: type[TemplateMethodComponent]
    ) -> TemplateMethodComponent:
        pass


class _LiteLLMComponentCreator(_ComponentCreator):
    def create_component(
        self, prompt: str, component_class: type[TemplateMethodComponent]
    ) -> TemplateMethodComponent:
        from litellm import completion

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


class _TrustcallComponentCreator(_ComponentCreator):
    def create_component(
        self, prompt: str, component_class: type[TemplateMethodComponent]
    ) -> TemplateMethodComponent:
        from trustcall import create_extractor

        model_response = create_extractor(
            self.model_name,
            tools=[component_class],
        ).invoke(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        return component_class(
            **json.loads(model_response.choices[0]["message"].content)
        )


class _LangchainComponentCreator(_ComponentCreator):
    def create_component(
        self, prompt: str, component_class: type[TemplateMethodComponent]
    ) -> TemplateMethodComponent:
        from langchain.chat_models import init_chat_model

        model_response = (
            init_chat_model(
                self.model_name,
            )
            .with_structured_output(component_class)
            .invoke(
                [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            )
        )
        return model_response


class TemplateMethodCreator(ABC):
    _component_creator: _ComponentCreator = _LiteLLMComponentCreator

    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def create(self) -> TemplateMethod:
        pass

    def _create_component(
        self, prompt: str, component_class: type[TemplateMethodComponent]
    ) -> TemplateMethodComponent:
        return self._component_creator(self.model_name).create_component(
            prompt, component_class
        )
