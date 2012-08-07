__author__ = 'maluuba'
from os.path import join
from jinja2 import Template

import IDLGenerator
def loadTemplate(name):
  templatePath = join('/'.join(IDLGenerator.__file__.split('/')[:-1]), 'templates', name)
  templateFile = open(templatePath, 'r')
  template = Template(templateFile.read())

  return template

if __name__ == '__main__':
  template = loadTemplate('Object.tpl')

  print template.render()