from __future__ import annotations

import json

import libcst
from _config import Config
from _convert_self2name import convert_self2name
from _template_method import TemplateMethod
from libcst import ClassDef
from libcst import FunctionDef
from libcst import Module
from litellm import completion


def split_long_function(
    function_def: FunctionDef, module: Module, config: Config
) -> "ClassDef":
    function_def = convert_self2name(function_def, module)
    function_code = Module([function_def]).code
    model_response = completion(
        messages=[
            {
                "role": "user",
                "content": (
                    "Your tasks is split a long function by converting it to template method. "
                    "\nAssume that all the variables are defined and no import is needed "
                    "unless explicit import is provided on the function level. "
                    "\nWhen creating calls take into account if functions are asynchronous add await or async for if needed. "
                    "\nFUNCTION:"
                    f"\n{function_code}"
                ),
            }
        ],
        model=config.model_name,
        response_format=TemplateMethod,
    )
    class_def = libcst.parse_statement(
        str(
            TemplateMethod(
                **json.loads(model_response.choices[0]["message"].content)
            )
        ).replace("\t", 4 * " ")
    )
    assert isinstance(
        class_def, ClassDef
    ), f"{split_long_function.__name__} failed to produce {ClassDef.__name__}. Produced {type(class_def).__name__} instead"
    return class_def
