__author__ = 'maluuba'
from boto import connect_s3
from IDLParser.parser import parse

if __name__ == '__main__':
  s3 = connect_s3()
  b = s3.get_bucket('maluuba-idl-templates')
  idls = b.get_all_keys(prefix='idl')
  idls = [idl for idl in idls if idl.name.endswith('.idl')]

  s = []
  f = []
  for idl in idls:
    try:
      idlContent = idl.get_contents_as_string()
      ast = parse(idlContent)
      for item in ast:
        #print item
        pass
      s.append(idl.name)
    except Exception, e:
      f.append(idl.name)
      #print e

  for n in s:
    print '%s passed my parser test!!!' % n
  for n in f:
    print '%s failed my parser test!!!' % n

