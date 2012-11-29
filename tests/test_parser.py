#!/usr/bin/env python

import unittest

from pyidl.parser import ast, parser


class TestSetup(object):
    """PyIDL Parser test cases."""

    def setUp(self):
        pass


class TestBaseMixin(object):

    def read_case(self, name):
        return file('tests/cases/%s.idl' % name, 'r').read()


class ParserTestSuite(TestSetup, TestBaseMixin, unittest.TestCase):

    def test_simple_enum(self):
        document = parser.parse(self.read_case('simple_enum'))
        assert len(document) == 1
        enum_parse = document[0]
        assert type(enum_parse) == ast.t_enum
        assert enum_parse.name == "SomeSet"
        assert set(enum_parse.values) == set([(x, None) for x in
            'A', 'B', 'C'])

    def test_complex_enum(self):
        document = parser.parse(self.read_case('complex_enum'))
        assert len(document) == 1
        enum_parse = document[0]
        assert type(enum_parse) == ast.t_enum
        assert enum_parse.name == "SomeSet"
        assert set(enum_parse.values) == set([
            ('A', 1),
            ('B', None),
            ('C', 4)])

    def test_simple_struct_with_namespace(self):
        document = parser.parse(self.read_case('simple_struct_with_namespace'))
        assert len(document) == 2

        namespace_parse = document[0]
        self.assertEquals(('namespace', 'java', 'pyidl.example'), namespace_parse)

        struct_parse = document[1]
        assert type(struct_parse) is ast.t_struct
        self.assertEquals('RequestObject', struct_parse.name)
        self.assertEquals(('someRequest', 1, 'string'), struct_parse.declaration_list[0])
        self.assertEquals(('someValue', 2, 'double'), struct_parse.declaration_list[1])

    def test_complex_struct(self):
        document = parser.parse(self.read_case('complex_struct'))
        #import pdb
        #pdb.set_trace()
        print document
