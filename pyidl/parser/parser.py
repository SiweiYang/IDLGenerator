#!/usr/bin/env python
from scanner import filterMultilineComment, filterInlineComment, supported_languages

__author__ = 'maluuba'
from scanner import lexer, tokens
from ply.yacc import yacc


def p_namespace_type(p):
  p[0] = p[1]
p_namespace_type.__doc__ = 'ns_type : %s' % '\n| '.join(supported_languages.values())


def p_namespace(p):
  'ns : namespace ns_type identifier'
  p[0] = (p[1], p[2], p[3])


def p_require(p):
  'req : require identifier'
  p[0] = (p[1], p[2])


def p_assignment(p):
  'assignment : identifier ASSIGN intconstant'
  p[0] = (p[1], int(p[3]))


def p_assignment_list(p):
  '''assignment_list : assignment
                     | assignment_list COMMA assignment'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]


def p_identifier_extended(p):
  '''identifier_extended : identifier
                         | Index
                         | Identifier'''
  p[0] = p[1]


def p_identifier_list(p):
  '''identifier_list : identifier
                     | identifier_list COMMA identifier'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]


def p_enum_list(p):
  '''enum_list : assignment
               | identifier
               | enum_list COMMA assignment
               | enum_list COMMA identifier'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]


def p_enum(p):
  '''enum : Enum identifier LCURLY enum_list RCURLY'''
  p[0] = ('enum', p[2], p[4])


def p_type(p):
  '''type : identifier
  | i32
  | i64
  | Boolean
  | Double
  | String
  | Object
  | Set LT type GT
  | List LT type GT
  | Map LT type COMMA type GT'''
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 5:
    p[0] = (p[1], p[3])
  elif len(p) == 7:
    p[0] = (p[1], p[3], p[5])


def p_declaration_basic(p):
  '''declaration_basic : type identifier
                 | RangeIndex type identifier
                 | Index type identifier'''
  if len(p) == 3:
    p[0] = (p[2], None, p[1])
  if len(p) == 4:
    p[0] = (p[3], None, p[2], p[1])


def p_declaration(p):
  '''declaration : declaration_basic
                 | intconstant SEMICOLON declaration_basic'''
  if len(p) == 2:
    p[0] = p[1]
  if len(p) == 4:
    p[3] = list(p[3])
    p[3][1] = int(p[1])
    p[0] = tuple(p[3])


def p_declaration_list(p):
  '''declaration_list : declaration
                      | declaration_list COMMA declaration'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]


def p_struct_annotation(p):
  '''struct_annotation : Struct identifier'''
  p[0] = (p[2])


def p_struct_annotation_response(p):
  '''struct_annotation : Struct identifier Response'''
  p[0] = (p[2], 'response')


def p_struct_annotation_persistent(p):
  '''struct_annotation : Struct identifier Persistent
                       | Struct identifier Persistent LPAREN identifier RPAREN
                       | Struct identifier Persistent LPAREN identifier COMMA identifier RPAREN'''
  if len(p) == 4:
    p[0] = (p[2], 'persistent', 'dynamo', p[2])
  if len(p) == 7:
    p[0] = (p[2], 'persistent', 'dynamo', p[5])
  if len(p) == 9:
    p[0] = (p[2], 'persistent', p[7], p[5])


def p_struct_basic(p):
  '''struct : struct_annotation LCURLY RCURLY
            | struct_annotation LCURLY declaration_list RCURLY'''
  if len(p) == 4:
    p[0] = ('struct', p[1], [])
  if len(p) == 5:
    p[0] = ('struct', p[1], p[3])


def p_function_basic(p):
  '''function_basic : type identifier_extended LPAREN RPAREN
                    | type identifier_extended LPAREN declaration_list RPAREN'''
  if len(p) == 5:
    p[0] = (p[2], p[1], [])
  if len(p) == 6:
    p[0] = (p[2], p[1], p[4])


def p_function_post(p):
  '''function : Post function_basic
              | function_basic'''
  if len(p) == 2:
    p[0] = p[1]
  if len(p) == 3:
    p[0] = p[2]


def p_function_list(p):
  '''function_list : function_list function COMMA
                   | function_list function COLON
                   | function_list function
                   | function COMMA
                   | function COLON
                   | function'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 3:
    if p[2] == ',':
      p[0] = [p[1]]
    elif p[2] == ';':
      p[0] = [p[1]]
    else:
      p[0] = p[1] + [p[2]]
  if len(p) == 4:
    p[0] = p[1] + [p[2]]


def p_service(p):
  'service : Service identifier LCURLY function_list RCURLY'
  p[0] = ('service', p[2], p[4])


def p_document(p):
  '''document : ns
              | req
              | enum
              | struct
              | service
              | document document'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 3:
    p[0] = p[1] + p[2]


def p_error(t):
  print("Syntax error at '%s'" % t.value)

start = 'document'
parser = yacc()


def parse(str):
  str = filterMultilineComment(str)
  str = filterInlineComment(str)
  return parser.parse(str)
