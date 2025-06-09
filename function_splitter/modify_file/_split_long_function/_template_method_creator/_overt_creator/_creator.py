from __future__ import annotations

from itertools import count

from _split_long_function._template_method import Constructor
from _split_long_function._template_method import Field
from _split_long_function._template_method import Method
from _split_long_function._template_method import TemplateMethod
from _split_long_function._template_method_creator._template_method_creator import (
    TemplateMethodCreator,
)
from libcst import FunctionDef
from libcst import Module
from pydantic import BaseModel
from pydantic import Field as PydanticField

from ._constructor_fields_extractor import constructor_fields_extractor
from ._variable_name_replacer import VariableNameReplacer


class OvertCreator(TemplateMethodCreator):
    def __init__(self, function_node: FunctionDef, model_name: str):
        super().__init__(model_name)
        self.function_node = function_node

    def create(self) -> TemplateMethod:
        replacer = VariableNameReplacer(self.function_node)
        self_function_code = Module([self.function_node.visit(replacer)]).code
        fields = list(
            _FieldAny(field_name=name) for name in replacer.replaced_names
        )
        constructor_fields = constructor_fields_extractor(self.function_node)
        constructor = Constructor(fields=list(constructor_fields))
        self_function_code_with_line_numbers = "\n".join(
            map("{}. {}".format, count(), self_function_code.splitlines())
        )
        missing_elements = self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "\nWhen creating calls in the main function take into account if functions are asynchronous add await or async for if needed. "
                "\nWhen creating calls in the main function take into account if functions are asynchronous add await or async for if needed. "
                "\nFUNCTION:"
                f"\n{self_function_code_with_line_numbers}"
            ),
            _MissingElements,
        )
        submethods = list(
            Method(
                code=f"def {submethod.function_name}(self):\n"
                + "\n".join(
                    self_function_code.splitlines()[
                        submethod.start_line : submethod.end_line + 1
                    ]
                )
            )
            for submethod in missing_elements.submethods
        )
        return TemplateMethod(
            constructor=constructor,
            name=missing_elements.class_name,
            fields=fields,
            submethods=submethods,
            main_method=missing_elements.main_method,
        )


class _FieldAny(Field):
    field_type: str = "Any"


class _Submethod(BaseModel):
    start_line: int = PydanticField(
        description="Number of the line from the input function that should be the first line of the submethod"
    )
    end_line: int = PydanticField(
        description="Number of the line from the input function that should be the last line of the submethod (inclusive)"
    )
    function_name: str


class _MissingElements(BaseModel):
    submethods: list[_Submethod]
    main_method: Method
    class_name: str
