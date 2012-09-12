__author__ = 'maluuba'

class Enum:
  def __init__(self, serviceID, version, ast):
    name, values = ast
    for i in range(len(values)):
      v = values[i]
      if type(v) == 'str':
        v = (v, i)
      values[i] = v
    self.name = name
    self.fields = [(value[0], 'string', value[1]) for value in values]

    pass

class Struct:
  def __init__(self, serviceID, version, ast):
    name, fields = ast
    if not type(name) == 'str':
      name, persistent, provider, table = name
    self.name = name
    self.fields = fields

class Function:
  def __init__(self, serviceID, version, ast):
    name, response, params = ast

class Service:
  def __init__(self, serviceID, version, ast):
    name, functions = ast
    functions = [Function(function) for function in functions]

