__author__ = 'maluuba'

def parameterList(fields):
  return ' ,'.join(['%s %s' % (fieldType, fieldName) for fieldType, fieldRealType, fieldMeta, fieldName in fields])