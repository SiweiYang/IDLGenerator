#!/usr/bin/env python
__author__ = 'maluuba'
from re import compile
from ply.lex import lex

supported_languages = {
  "as3": "as3",
  "c_glib": "c_glib",
  "cpp": "cpp",
  "csharp": "csharp",
  "erl": "erl",
  "hs": "hs",
  "java": "java",
  "js": "js",
  "cocoa": "cocoa",
  "ocaml": "ocaml",
  "perl": "perl",
  "php": "php",
  "py": "py",
  "rb": "rb",
  "st": "st"
}

reserved = dict(supported_languages.items() + {
  "namespace"   : 'namespace',
  "require"     : 'require',
  "include"     : 'include',
  "import"      : 'import',
  "void"        : 'void',
  "bool"        : 'Boolean',
  "i32"         : 'i32',
  "i64"         : 'i64',
  "double"      : 'Double',
  "string"      : 'String',
  "object"      : 'Object',
  "map"         : 'Map',
  "list"        : 'List',
  "set"         : 'Set',
  "enum"        : 'Enum',
  "post"        : 'Post',
  "struct"      : 'Struct',
  "persistent"  : 'Persistent',
  "response"    : 'Response',
  "service"     : 'Service',
  "identifier"  : 'Identifier',
  "index"       : 'Index',
  "range-index" : 'RangeIndex'
}.items())

tokens = list(reserved.values()) + [
  'intconstant',
  'identifier',
#  'whitespace',
#  'sillycomm',
#  'doctext',
#  'comment',
#  'unixcomment',
  'SEMICOLON',
  'COLON',
  'COMMA',
  'LPAREN',
  'RPAREN',
  'LCURLY',
  'RCURLY',
  'ASSIGN',
  'LT',
  'GT',
  'QUOTATION',
#  'symbol'
]


def t_identifier(t):
  r'[a-zA-Z_][\-\.a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'identifier')
  return t

t_intconstant   = r'[+-]?[0-9]+'
#t_whitespace    = r'[ \t\r\n]+'
#t_sillycomm     = r'"/*""*"*"*/"'
#t_doctext       = r'"/**"([^*/]|[^*]"/"|"*"[^/])*"*"*"*/"'
#t_comment       = r'//[^\n]*'
#t_unixcomment   = r'\#[^\n]*'
t_SEMICOLON     = r':'
t_COLON         = r';'
t_COMMA         = r','
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LCURLY        = r'{'
t_RCURLY        = r'}'
t_ASSIGN        = r'\='
t_GT            = r'>'
t_LT            = r'<'
t_QUOTATION     = r'"'
#t_symbol        = r'[:;\,\{\}\(\)\=<>\[\]]'

#t_ignore        = '[ \t\r\n]+'
t_ignore        = '[ \t\r\n]+'

lexer = lex()

def filterMultilineComment(str):
  t_multicomm     = r'/\*([^*]*\*)(([^*/][^*]*)?\*)*/'
  p = compile(t_multicomm)
  return p.sub(' ', str)

def filterInlineComment(str):
  t_singlecomm     = r'//[^\n]*'
  p = compile(t_singlecomm)
  return p.sub(' ', str)