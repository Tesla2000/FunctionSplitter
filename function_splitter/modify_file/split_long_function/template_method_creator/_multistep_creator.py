from __future__ import annotations

from function_splitter.modify_file.split_long_function.template_method_components import (
    TemplateMethod,
)
from function_splitter.modify_file.split_long_function.template_method_creator._get_constructor_and_fields import (
    get_constructor_and_fields,
)
from function_splitter.modify_file.split_long_function.template_method_creator._template_method_creator import (
    TemplateMethodCreator,
)
from libcst import FunctionDef


class MultistepCreator(TemplateMethodCreator):
    def __init__(self, function_def: FunctionDef, model_name: str):
        super().__init__(model_name)
        self.function_def = function_def

    def create(self) -> TemplateMethod:
        constructor, self_fields, self_function_code = (
            get_constructor_and_fields(self.function_def)
        )
        from litellm import completion

        content = ""
        messages = [
            {
                "role": "user",
                "content": (
                    "Your tasks is split a long function by converting it to template method."
                    "\nAssume that all the variables are defined and no import is needed "
                    "unless explicit import is provided on the function level."
                    "\nMake the main method public and submethod private (mark with _)."
                    "\nConstructor of the template method should contain the same parameters as the original function."
                    "\nWhen creating calls take into account if functions are asynchronous add await or async for if needed."
                    "\nMark output template method with <code>...</code> with the template method between. Return only the template method without comments."
                    "\nIMPORTANT: Every line of the original function must be present in the template method."
                    "\nFUNCTION:"
                    f"\n{self_function_code}"
                ),
            }
        ]
        while True:
            model_response = completion(
                messages=messages,
                model=self.model_name,
            )
            model_extra = model_response.choices[0].model_extra
            part = model_extra["message"].content
            if "<code>" in part and "</code>" in part:
                content += part.split("<code>")[1].split("</code>")[0]
                break
            elif "<code>" in part:
                content += part.split("<code>")[1]
            elif "</code>" in part:
                content += part.split("</code>")[0]
                break
            else:
                content += part
            if model_extra["finish_reason"] == "stop":
                break
            messages.append(
                {
                    "role": "assistant",
                    "content": part,
                }
            )
            messages.append(
                {
                    "role": "user",
                    "content": "Continue",
                }
            )
            messages[0]["role"] = "system"
        # return TemplateMethod(
        #     constructor=constructor,
        #     main_method=missing_elements.main_method,
        #     submethods=missing_elements.submethods,
        #     fields=missing_elements.fields,
        #     name=missing_elements.class_name,
        # )
