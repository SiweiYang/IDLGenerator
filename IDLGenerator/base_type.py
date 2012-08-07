__author__ = 'maluuba'
from sys import stdout
from IDLGenerator.generator import loadTemplate

class BaseType:
  def __init__(self, package, type, imports = [], fields = [], persistent = ()):
    self.package, self.type, self.imports, self.fields, self.persistent = package, type, imports, fields, persistent

  def generate(self, file=stdout):
    package, type, imports, fields, persistent = self.package, self.type, self.imports, self.fields, self.persistent
    template = loadTemplate('Object.tpl')
    file.write(template.render(package = package, type = type, imports = imports, fields = fields, persistent = persistent))
