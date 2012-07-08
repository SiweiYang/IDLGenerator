#!/usr/bin/env python
__author__ = 'maluuba'
from scanner import lexer, tokens
from ply.yacc import yacc

def p_assignment(p):
  'assignment : identifier ASSIGN intconstant'
  p[0] = (p[1], p[3])

def p_custom_type(p):
  'type : identifier'
  p[0] = p[1]

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
  '''struct_basic : struct_annotation LPAREN RPAREN COLON
                  | struct_annotation LPAREN declaration_list RPAREN COLON'''
  if len(p) == 5:
    p[0] = (p[1], [])
  if len(p) == 6:
    p[0] = (p[1], p[4])

def p_function_basic(p):
  '''function_basic : identifier identifier LPAREN RPAREN COLON
                    | identifier identifier LPAREN declaration_list RPAREN COLON'''
  if len(p) == 6:
    p[0] = (p[2], p[1], [])
  if len(p) == 7:
    p[0] = (p[2], p[1], p[4])

def p_function_post(p):
  '''function : Post function_basic
              | function_basic'''
  if len(p) == 2:
    p[0] = p[1]
  if len(p) == 3:
    p[0] = p[2]

def p_function_list(p):
  '''function_list : function_list function
                   | function'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 3:
    p[0] = p[1] + [p[2]]

def p_service(p):
  'service : Service identifier LCURLY function_list RCURLY'
  p[0] = (p[2], p[4])

def p_error(t):
  print("Syntax error at '%s'" % t.value)

start = 'service'
parser = yacc()

if __name__ == '__main__':
  print parser.parse('''
  service Routing {
    post SetRouteResponse setRoute(1: RoutingTableEntry route);
    ListRoutesResponse listRoutes();
    post SetRouteResponse setRoute(1: RoutingTableEntry route);
    post SetRouteEndpointResponse setRouteEndpoint(1: string routeId, 2: Endpoint endpoint, 3: string path);
    GetRouteResponse getRoute(1: string routeId);
    ListRoutesResponse listRoutes();
  }
  ''')