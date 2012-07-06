#!/usr/bin/env python
__author__ = 'maluuba'
from ply.lex import lex

reserved = {
  "namespace"   : 'namespace',
  "persistent"  : 'persistent',
  "response"    : 'response',
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
  "post"        : 'post',
  "struct"      : 'struct',
  "service"     : 'service',
  "identifier"  : 'Identifier',
  "index"       : 'Index',
  "range-index" : 'RangeIndex'
}

tokens = list(reserved.values()) + [
  'intconstant',
  'identifier',
#  'whitespace',
#  'sillycomm',
#  'multicomm',
#  'doctext',
#  'comment',
#  'unixcomment',
  'SEMICOLON',
  'COMMA',
  'ASSIGN',
  'GT',
  'LT',
#  'symbol'
]

def t_identifier(t):
  r'[a-zA-Z_][\-\.a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'identifier')
  return t

t_intconstant   = r'[+-]?[0-9]+'
#t_whitespace    = r'[ \t\r\n]+'
#t_sillycomm     = r'"/*""*"*"*/"'
#t_multicomm     = r'/*"[^*]"/"*([^*/]|[^*]"/"|"*"[^/])*"*"*"*/"'
#t_doctext       = r'"/**"([^*/]|[^*]"/"|"*"[^/])*"*"*"*/"'
#t_comment       = r'//[^\n]*'
#t_unixcomment   = r'\#[^\n]*'
t_SEMICOLON     = r':'
t_COMMA         = r','
t_ASSIGN        = r'\='
t_GT            = r'>'
t_LT            = r'<'
#t_symbol        = r'[:;\,\{\}\(\)\=<>\[\]]'

t_ignore        = r'[ \t\r\n]+'

lexer = lex()


