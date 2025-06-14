from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from pydantic import Field as PydanticField

from ._constructor import Constructor
from ._field import Field
from ._main_method import MainMethod
from ._method import Method


class TemplateMethodNameAndFields(BaseModel):
    name: str = PydanticField(
        description="Name of the template method that describes it's purpose"
    )
    fields: list[Field] = PydanticField(
        description="List of fields of the class that are used to pass data between methods. Should be private"
    )

    def __str__(self):
        return f"Name: {self.name}\nFields:{'\n'.join(map(str, self.fields))}"


class TemplateMethodConstructor(BaseModel):
    constructor: Constructor = PydanticField(
        description="Constructor method. Should contain field corresponding to the parameters of the original function"
    )

    def __str__(self):
        return str(self.constructor)


class TemplateMethodSubmethods(BaseModel):
    submethods: list[Method] = PydanticField(
        description="Private methods of the class each responsible for a specific piece of code. A few logical lines tops. Modify self fields and likely don't return values"
    )

    def __str__(self):
        return "\n".join(map(str, self.submethods))


class TemplateMethodMainMethod(BaseModel):
    main_method: MainMethod = PydanticField(
        description="The only public method of the class should contain calls to all submethods in the correct order and return correct values"
    )

    def __init__(self, /, **data: Any):
        main_method_code = data["main_method"]
        if isinstance(main_method_code, str):
            data["main_method"] = MainMethod(code=main_method_code)
        super().__init__(**data)

    def __str__(self):
        return str(self.main_method)


class TemplateMethod(
    TemplateMethodNameAndFields,
    TemplateMethodConstructor,
    TemplateMethodSubmethods,
    TemplateMethodMainMethod,
):
    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.submethods = list(
            submethod
            for submethod in self.submethods
            if submethod.function_def.name.value != object.__init__.__name__
        )

    def __str__(self):
        return f"""class {self.name}:
    {'\n\t'.join(map(str, self.fields))}

{str(self.constructor)}

{str(self.main_method)}

{'\n'.join(map(str, self.submethods))}"""
