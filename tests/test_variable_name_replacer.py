from __future__ import annotations

import unittest

import libcst
from function_splitter.modify_file.split_long_function.template_method_creator._variable_name_replacer import (
    VariableNameReplacer,
)
from libcst import FunctionDef


class TestVariableNameReplacer(unittest.TestCase):
    def test_variable_name_replacer_walrus(self):
        function_code = """async def generate_retirement_response(self):
        if (savings := 1):
            pass"""
        module = libcst.parse_module(function_code)
        function_def = module.body[0]
        self.assertIsInstance(function_def, FunctionDef)
        self.assertEqual(
            function_code,
            module.visit(VariableNameReplacer(function_def)).code,
        )
