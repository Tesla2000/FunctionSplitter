from __future__ import annotations

from collections.abc import Mapping
from typing import Optional

from libcst import ClassDef
from libcst import CSTTransformer
from libcst import CSTVisitor
from libcst import FunctionDef
from libcst import IndentedBlock
from libcst import Module
from libcst import parse_statement
from libcst import Yield


def function2template_method(
    replacements: Mapping["FunctionDef", "ClassDef"], module: Module
) -> Module:
    user_classes = []

    class Transformer(CSTTransformer):
        def leave_FunctionDef(
            self, original_node: "FunctionDef", updated_node: "FunctionDef"
        ) -> "FunctionDef":
            if not (class_def := replacements.get(original_node)):
                return updated_node
            user_classes.append(class_def)
            main_function = next(
                filter(
                    lambda line_statement: isinstance(
                        line_statement, FunctionDef
                    )
                    and not line_statement.name.value.startswith("_"),
                    class_def.body.body,
                )
            )
            is_async = bool(main_function.asynchronous)
            is_generator = _is_generator(main_function)
            call = f"{class_def.name.value}({', '.join(param.name.value for param in updated_node.params.params)}).{main_function.name.value}()"
            if is_async and is_generator:
                statement = f"async for _ in {call}:\n\tyield _"
            elif is_async:
                statement = f"return await {call}"
            elif is_generator:
                statement = f"return yield from {call}"
            else:
                statement = f"return {call}"
            return updated_node.with_changes(
                body=IndentedBlock([parse_statement(statement)])
            )

    updated_module = module.visit(Transformer())
    return updated_module.with_changes(
        body=(*updated_module.body, *user_classes)
    )


def _is_generator(function_def: FunctionDef) -> bool:
    class IsGeneratorException(Exception):
        pass

    class Visitor(CSTVisitor):
        def visit_Yield(self, node: "Yield") -> Optional[bool]:
            raise IsGeneratorException

    try:
        function_def.visit(Visitor())
        return False
    except IsGeneratorException:
        return True
