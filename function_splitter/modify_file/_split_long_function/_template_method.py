from __future__ import annotations

from typing import Any
from typing import Optional

import libcst
from libcst import FunctionDef
from pydantic import BaseModel
from pydantic import Field as PydanticField


class Method(BaseModel):
    code: str = PydanticField(
        description=(
            "Method code should include definition, name only self in args "
            "(there rest should be provided as fields in self). "
            "Return values if needed but operating mostly on self fields."
            "Create neither docstrings not comments."
        )
    )

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        function_def = libcst.parse_statement(self.code)
        assert isinstance(function_def, FunctionDef)

    def __str__(self):
        return "".join(map("\n\t".__add__, self.code.splitlines()))


class Field(BaseModel):
    field_name: str
    field_type: Optional[str]

    def __str__(self):
        if self.field_type:
            return f"{self.field_name}: {self.field_type}"
        return self.field_name


class Constructor(BaseModel):
    fields: list[Field] = PydanticField(
        description=(
            "Fields user by constructor. each fields corresponds to constructor assignment."
            "\nExample:"
            "\nFields: [{'field_name': 'foo', 'field_type': 'int'}, {'field_name': 'bar', 'field_type': 'str'}]"
            "\nWill create constructor:"
            "\ndef __init__(self, foo: int, bar: str):"
            "\n\tself.foo: int = foo"
            "\n\tself.bar: str = bar"
        )
    )

    def __str__(self):
        return (
            f"\tdef __init__(self, {', '.join(map(str, self.fields))}):"
            + "".join(
                f"\n\t\tself.{field} = {field.field_name}"
                for field in self.fields
            )
        )


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
    main_method: Method = PydanticField(
        description="The only public method of the class should contain calls to all submethods in the correct order and return correct values"
    )

    def __init__(self, /, **data: Any):
        main_method_code = data["main_method"]
        if isinstance(main_method_code, str):
            data["main_method"] = Method(code=main_method_code)
        super().__init__(**data)

    def __str__(self):
        return str(self.main_method)


class TemplateMethod(
    TemplateMethodNameAndFields,
    TemplateMethodConstructor,
    TemplateMethodSubmethods,
    TemplateMethodMainMethod,
):
    def __str__(self):
        return f"""class {self.name}:
    {'\n\t'.join(map(str, self.fields))}

{str(self.constructor)}

{str(self.main_method)}

{'\n\n'.join(map(str, self.submethods))}"""
