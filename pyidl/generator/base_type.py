from generator import util

__author__ = 'maluuba'
from sys import stdout
from generator.generator import loadTemplate

class BaseType:
  def __init__(self, package, type, imports = [], fields = [], persistent = ()):
    self.package, self.type, self.imports, self.fields, self.persistent = package, type, imports, fields, persistent

  def generate(self, file=stdout):
    package, type, imports, fields, persistent = self.package, self.type, self.imports, self.fields, self.persistent

    template = loadTemplate('Object.tpl')
    if persistent[1] == 'dynamo':
      template = loadTemplate('DynamoObject.tpl')
    if persistent[1] == 'mongo':
      template = loadTemplate('MongoObject.tpl')

    file.write(template.render(package = package, type = type, imports = imports, fields = fields, persistent = persistent, helper = util))

if __name__ == '__main__':
  bt= BaseType('org.maluuba.service.generator', 'Generator', [], [('int', 'int', {}, 'a'), ('Map<String, String>', 'Map', {}, 'b')], ('test', 'mongo'))
  bt.generate()