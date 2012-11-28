#!/usr/bin/env python

import unittest

from pyidl.parser import parser


class TestSetup(object):
    """PyIDL Parser test cases."""

    def setUp(self):
        pass


class TestBaseMixin(object):

    def read_case(self, name):
        return file('tests/cases/%s.idl' % name, 'r').read()


class ParserTestSuite(TestSetup, TestBaseMixin, unittest.TestCase):

    def test_simple_enum(self):
        ast = parser.parse(self.read_case('simple_enum'))
        self.assertEquals(1, len(ast))
        enum_parse = ast[0]
        self.assertEquals('enum', enum_parse[0])
        self.assertEquals('Subgroup', enum_parse[1])
        self.assertEquals(set([
            'MUSIC_SONG_REMOVE',
            'MUSIC_SONG_INFO',
            'MUSIC_SONG_PAUSE',
            'MUSIC_RADIO',
            'MUSIC_SONG_RATING',
            'MUSIC_SONG_RESET',
            'MUSIC_SONG_RESUME',
            'MUSIC_SONG_PLAY'
            ]), set(enum_parse[2]))

    def test_simple_struct_with_namespace(self):
        ast = parser.parse(self.read_case('simple_struct_with_namespace'))
        self.assertEquals(2, len(ast))

        namespace_parse = ast[0]
        self.assertEquals(('namespace', 'pyidl.example'), namespace_parse)

        struct_parse = ast[1]
        self.assertEquals('struct', struct_parse[0])
        self.assertEquals('RequestObject', struct_parse[1])
        self.assertEquals(('someRequest', 1, 'string'), struct_parse[2][0])
        self.assertEquals(('someValue', 2, 'double'), struct_parse[2][1])

    def test_complex_struct(self):
        ast = parser.parse(self.read_case('complex_struct'))
        print ast
