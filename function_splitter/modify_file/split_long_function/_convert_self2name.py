from __future__ import annotations

from typing import Optional
from typing import TypeVar

from libcst import Annotation
from libcst import ClassDef
from libcst import CSTNode
from libcst import CSTTransformer
from libcst import FunctionDef
from libcst import Module
from libcst import Name
from libcst import Param
from libcst import SimpleString
from utility_functions import camelcase2snakecase


def convert_self2name(
    function_def: FunctionDef, module: Module
) -> FunctionDef:
    if _is_static(function_def):
        return function_def

    class Transformer(CSTTransformer):
        def __init__(self):
            super().__init__()
            self.parameter2class: dict["Param", "ClassDef"] = {}

        def visit_ClassDef(self, node: "ClassDef") -> Optional[bool]:
            function = next(filter(function_def.__eq__, node.body.body), None)
            if function is not None:
                self.parameter2class[function_def.params.params[0]] = node
            return super().visit_ClassDef(node)

        def leave_Param(
            self, original_node: "Param", updated_node: "Param"
        ) -> "Param":
            if class_ := self.parameter2class.get(original_node):
                class_name = class_.name.value
                return updated_node.with_changes(
                    name=Name(self._class_name2self(class_name)),
                    annotation=Annotation(
                        annotation=SimpleString(f'"{class_name}"')
                    ),
                )
            return updated_node

        def leave_FunctionDef(
            self, original_node: "FunctionDef", updated_node: "FunctionDef"
        ) -> "FunctionDef":
            nonlocal function_def
            if original_node is function_def:
                for param, class_ in self.parameter2class.items():
                    class_name = class_.name.value
                    updated_node = _replace_names(
                        updated_node,
                        param.name.value,
                        self._class_name2self(class_name),
                    )
                function_def = updated_node
            return updated_node

        @staticmethod
        def _class_name2self(class_name: str) -> str:
            return camelcase2snakecase(class_name)

    module.visit(Transformer())
    return function_def


def _is_static(function_def: FunctionDef) -> bool:
    return any(
        decorator.decorator.value == staticmethod.__name__
        for decorator in function_def.decorators
        if isinstance(decorator.decorator, Name)
    )


NodeType = TypeVar("NodeType", bound=CSTNode)


def _replace_names(
    node: NodeType, prev_name_value: str, new_name_value: str
) -> NodeType:
    class Transformer(CSTTransformer):
        def leave_Name(
            self, original_node: "Name", updated_node: "Name"
        ) -> "Name":
            if original_node.value == prev_name_value:
                return Name(new_name_value)
            return updated_node

    return node.visit(Transformer())
