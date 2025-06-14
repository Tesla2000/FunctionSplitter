from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Field(BaseModel):
    field_name: str
    field_type: Optional[str]

    def __str__(self):
        if self.field_type:
            return f"{self.field_name}: {self.field_type}"
        return self.field_name
