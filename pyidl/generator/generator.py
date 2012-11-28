__author__ = 'maluuba'
from os.path import join
from jinja2 import Template, Environment, PackageLoader

import generator

env = Environment(loader=PackageLoader('IDLGenerator', 'templates'))
def loadTemplate(name):
  templatePath = join('/'.join(IDLGenerator.__file__.split('/')[:-1]), 'templates', name)
  templateFile = open(templatePath, 'r')
  #template = Template(templateFile.read())
  template = env.get_template(name)

  return template

if __name__ == '__main__':
  template = loadTemplate('Object.tpl')

  print template.render()