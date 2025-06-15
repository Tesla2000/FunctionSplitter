from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field as PydanticField


class Field(BaseModel):
    field_name: str = PydanticField(description="Should be private")
    field_type: str

    def __str__(self):
        return f"{self.field_name}: {self.field_type}"
