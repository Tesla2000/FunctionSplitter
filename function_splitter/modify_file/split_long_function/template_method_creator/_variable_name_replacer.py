from __future__ import annotations

from typing import Union

import libcst
from libcst import Arg
from libcst import BaseExpression
from libcst import FlattenSentinel
from libcst import FunctionDef
from libcst import Name
from libcst import Param
from libcst import Parameters
from libcst import RemovalSentinel


class VariableNameReplacer(libcst.CSTTransformer):

    def __init__(self, main_function: FunctionDef):
        super().__init__()
        self.main_function = main_function
        self.replaced_names: set[str] = set(
            param.name.value for param in self.main_function.params.params
        )

    def _self_name_creator(self, name: libcst.Name) -> libcst.Attribute:
        self.replaced_names.add(name.value)
        return libcst.Attribute(value=libcst.Name("self"), attr=name)

    def _replace_target(
        self, node: libcst.BaseExpression
    ) -> libcst.BaseExpression:
        if isinstance(node, libcst.Name):
            return self._self_name_creator(node)
        elif isinstance(node, (libcst.Tuple, libcst.List)):
            return node.with_changes(
                elements=[
                    elt.with_changes(value=self._replace_target(elt.value))
                    for elt in node.elements
                ]
            )
        return node

    def leave_FunctionDef(
        self, original_node: "FunctionDef", updated_node: "FunctionDef"
    ) -> "FunctionDef":
        if original_node is not self.main_function:
            return updated_node
        return updated_node.with_changes(
            params=Parameters((Param(name=Name("self")),))
        )

    def leave_Assign(
        self, original_node: libcst.Assign, updated_node: libcst.Assign
    ) -> libcst.Assign:
        new_targets = [
            assign.with_changes(target=self._replace_target(assign.target))
            for assign in updated_node.targets
        ]
        return updated_node.with_changes(targets=new_targets)

    def leave_Name(
        self, original_node: "Name", updated_node: "Name"
    ) -> "BaseExpression":
        if original_node.value in self.replaced_names:
            return self._self_name_creator(updated_node)
        return updated_node

    def leave_Arg(
        self, original_node: "Arg", updated_node: "Arg"
    ) -> Union["Arg", FlattenSentinel["Arg"], RemovalSentinel]:
        if isinstance(updated_node.keyword, libcst.Attribute):
            return updated_node.with_changes(keyword=updated_node.keyword.attr)
        return updated_node

    def leave_AugAssign(
        self, original_node: libcst.AugAssign, updated_node: libcst.AugAssign
    ) -> libcst.AugAssign:
        return updated_node.with_changes(
            target=self._replace_target(updated_node.target)
        )

    def leave_For(
        self, original_node: libcst.For, updated_node: libcst.For
    ) -> libcst.For:
        return updated_node.with_changes(
            target=self._replace_target(updated_node.target)
        )

    def leave_With(
        self, original_node: libcst.With, updated_node: libcst.With
    ) -> libcst.With:
        new_items = []
        for item in updated_node.items:
            if item.asname:
                new_asname = item.asname.with_changes(
                    name=self._self_name_creator(item.asname.name)
                )
                new_items.append(item.with_changes(asname=new_asname))
            else:
                new_items.append(item)
        return updated_node.with_changes(items=new_items)

    def leave_NamedExpr(
        self, original_node: libcst.NamedExpr, updated_node: libcst.NamedExpr
    ) -> libcst.NamedExpr:
        return updated_node.with_changes(
            target=self._replace_target(updated_node.target)
        )
