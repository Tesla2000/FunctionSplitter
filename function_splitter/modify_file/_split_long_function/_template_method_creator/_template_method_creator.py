from __future__ import annotations

import json
from abc import ABC
from abc import abstractmethod
from typing import TypeVar

from _split_long_function._template_method import TemplateMethod
from litellm import completion
from pydantic import BaseModel

TemplateMethodComponent = TypeVar("TemplateMethodComponent", bound=BaseModel)


class TemplateMethodCreator(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def create(self) -> TemplateMethod:
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
