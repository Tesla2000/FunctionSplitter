from __future__ import annotations

from function_splitter._config import Config
from function_splitter.modify_file.split_long_function.template_method_components import (
    MainMethod,
)
from function_splitter.modify_file.split_long_function.template_method_components import (
    TemplateMethod,
)
from libcst import FunctionDef
from pydantic import BaseModel
from pydantic import Field

from ._get_constructor_and_fields import get_constructor_and_fields
from ._overt_creator._elements import FieldAny
from ._template_method_creator import TemplateMethodCreator


class StepByStepCreator(TemplateMethodCreator):
    def __init__(
        self, config: Config, function_def: FunctionDef, function_code: str
    ):
        super().__init__(config.model_name)
        self.function_def = function_def
        self.function_code = function_code
        self.max_split_attempts = config.max_iterations

    def create(self) -> TemplateMethod:
        code = self.function_code
        passed_code = self.function_code
        main_function_name = self.function_def.name.value
        functions = []
        for _ in range(self.max_split_attempts):
            component = self._create_component(
                (
                    f"Your tasks is split a long function {main_function_name} into functions each a few lines tops."
                    "\nAssume that all the variables are defined and no import is needed unless explicit import is provided on the function level. "
                    "\nWhen creating calls in the main function take into account if functions are asynchronous add await or async for if needed. "
                    # f"\nDon't re-define already created functions list of already created functions is {', '.join(re.findall(r'def ([^\(]+)', function)[0] for function in functions)}. "
                    "```python"
                    f"\n{passed_code}\n"
                    "```\n"
                    f"Return:"
                    f"\n1. Fragment of the {main_function_name} that is to be replaced by function call. Note: only provide lines that are to be replaced. You mustn't provide the main function definition there. The part you provide must be 1:1 copy of the original"
                    f"\n2. Function call that is to replace the fragment."
                    f"\n3. Function that is a part of the code."
                    f"\n4. Boolean that indicates wherever further split are needed."
                ),
                _Step,
            )
            if (
                component.main_function_part not in code
                or component.main_function_part not in passed_code
            ):
                break
            code = code.replace(
                component.main_function_part, component.function_call
            )
            passed_code = passed_code.replace(component.main_function_part, "")
            functions.append(component.function)
            if not component.further_splits_needed:
                break
        functions.append(component.function)
        constructor, self_names, self_function_code = (
            get_constructor_and_fields(self.function_def)
        )
        fields = tuple(FieldAny(field_name=name) for name in self_names)
        function_code = self.function_code
        TemplateMethod(
            fields=fields,
            constructor=constructor,
            main_method=MainMethod(code=self_function_code),
            submethods=[],
            name="TemplateMethod",
        )
        name_and_fields = self._create_name_and_fields(function_code)
        constructor = self._create_constructor(function_code, name_and_fields)
        submethods = self._create_submethods(
            function_code, name_and_fields, constructor
        )
        main_method = self._create_main_method(
            function_code, name_and_fields, constructor, submethods
        )
        return TemplateMethod(
            name=name_and_fields.name,
            fields=name_and_fields.fields,
            constructor=constructor.constructor,
            submethods=submethods.submethods,
            main_method=main_method.main_method,
        )


class _Step(BaseModel):
    main_function_part: str = Field(
        description="It must be a 1:1 copy of the part of the main function that will be replaced by the call"
    )
    function_call: str = Field(
        description="Call to the new function that is to replace a part of the main function. Must take into account indentation and return variables if any"
    )
    function: str = Field(
        description="Function that is to replace the main function part"
    )
    further_splits_needed: bool = Field(
        description="Whether the further splits will be needed after the replace"
    )
