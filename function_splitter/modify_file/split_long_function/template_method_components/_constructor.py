from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field as PydanticField

from ._field import Field


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
                f"\n\t\tself._{field} = {field.field_name}"
                for field in self.fields
            )
        )
