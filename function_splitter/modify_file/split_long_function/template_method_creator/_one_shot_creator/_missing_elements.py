from __future__ import annotations

from typing import Any

from modify_file.split_long_function.template_method_components import Field
from modify_file.split_long_function.template_method_components import (
    MainMethod,
)
from modify_file.split_long_function.template_method_components import Method
from pydantic import BaseModel
from pydantic import Field as PydanticField


class _MissingElements(BaseModel):
    main_method: MainMethod = PydanticField(description="Must be public")
    submethods: list[Method] = PydanticField(
        description="Private methods of the class each responsible for a specific piece of code. A few logical lines tops. Modify self fields and likely don't return values"
    )
    fields: list[Field] = PydanticField(
        description="List of fields of the class that are used to pass data between methods. Should be private"
    )
    class_name: str

    def __init__(self, /, **data: Any):
        main_method = data["main_method"]
        if isinstance(main_method, str):
            data["main_method"] = MainMethod(code=main_method)
        super().__init__(**data)
