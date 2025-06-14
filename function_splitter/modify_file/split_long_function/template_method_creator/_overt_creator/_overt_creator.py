from __future__ import annotations

import sys
from itertools import filterfalse
from typing import Optional

from exceptions import NotAble2SplitException
from libcst import FunctionDef
from modify_file.split_long_function.template_method_components import Method
from modify_file.split_long_function.template_method_components import (
    TemplateMethod,
)
from modify_file.split_long_function.template_method_creator._get_constructor_and_fields import (
    get_constructor_and_fields,
)
from modify_file.split_long_function.template_method_creator._template_method_creator import (
    TemplateMethodCreator,
)
from pydantic import create_model
from pydantic.fields import Field

from ._elements import FieldAny
from ._elements import MissingElements


class OvertCreator(TemplateMethodCreator):
    def __init__(
        self,
        function_node: FunctionDef,
        model_name: str,
        submethod_creation_step: int,
    ):
        super().__init__(model_name)
        self.submethod_creation_step = submethod_creation_step
        self.function_node = function_node

    def create(self) -> TemplateMethod:
        constructor, self_names, self_function_code = (
            get_constructor_and_fields(self.function_node)
        )
        fields = tuple(FieldAny(field_name=name) for name in self_names)
        # self_function_code_with_line_numbers = "\n".join(
        #     map("{}. {}".format, count(), self_function_code.splitlines())
        # )
        missing_elements = self._create_component(
            (
                "Your tasks is split a long function by converting it to template method. "
                "\nAssume that all the variables are defined and no import is needed "
                "unless explicit import is provided on the function level. "
                "\nWhen creating calls in the main function take into account if functions are asynchronous add await or async for if needed. "
                "\nImportant: Methods you use in main method must be defined as submethods. Submethods should be short self-contained parts of code. You must ALWAYS provide submethods, main method and class name"
                "\nFUNCTION:"
                f"\n{self_function_code}"
            ),
            MissingElements,
        )
        gathered_submethods = {}
        missing_submethod_names = tuple(
            name.lstrip("_")
            for name in missing_elements.field_and_method_names
            if name not in self_names
        )
        n_missing_submethods = sys.maxsize
        while (
            missing_submethod_names
            and len(missing_submethod_names) < n_missing_submethods
        ):
            n_missing_submethods = len(missing_submethod_names)
            submethods_class = create_model(
                "Submethods",
                **{
                    submethod_name: (
                        Optional[str],
                        Field(
                            default=None,
                            description="Function including definition def foo(self)",
                        ),
                    )
                    for submethod_name in missing_submethod_names[
                        : self.submethod_creation_step
                    ]
                },
            )
            submethods = self._create_component(
                (
                    "Your tasks is split a long function by converting it to template method. "
                    "You are given original function and main function of the template method. "
                    "You must map original function to submethods of the main function"
                    "\nORIGINAL FUNCTION:"
                    f"\n{self_function_code}"
                    "\n\n\nMAIN METHODS:"
                    f"\n{missing_elements.main_method}"
                ),
                submethods_class,
            )
            gathered_submethods.update(
                submethods.model_dump(exclude_defaults=True)
            )
            missing_submethod_names = tuple(
                filterfalse(
                    submethods.model_dump(exclude_defaults=True).__contains__,
                    missing_submethod_names,
                )
            )
        if missing_submethod_names:
            raise NotAble2SplitException("Failed to extract submethods")
        return TemplateMethod(
            constructor=constructor,
            name=missing_elements.class_name,
            fields=fields,
            submethods=list(
                Method(code=submethod)
                for submethod in gathered_submethods.values()
            ),
            main_method=missing_elements.main_method,
        )
