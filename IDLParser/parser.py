#!/usr/bin/env python
__author__ = 'maluuba'
from scanner import lexer, tokens
from ply.yacc import yacc

def p_assignment(p):
  'assignment : identifier ASSIGN intconstant'
  p[0] = (p[1], p[3])

def p_type(p):
  '''type : Boolean
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

def p_declaration(p):
  'declaration : intconstant SEMICOLON type identifier'
  p[0] = (p[1], p[3])

def p_declaration_list(p):
  '''declaration_list : declaration
                      | declaration_list COMMA declaration'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]

def p_error(t):
  print("Syntax error at '%s'" % t.value)

start = 'declaration_list'
parser = yacc()

if __name__ == '__main__':
  parser.parse('bool')