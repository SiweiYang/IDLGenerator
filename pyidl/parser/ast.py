class t_program(object):

    def __init__(self, __ns=[], require=[], struct=[], enum=[], service=[]):
        self.namespace = {n.lang: n for n in __ns}
        self.__ns = __ns
        self.struct = struct
        self.enum = enum
        self.service = service


class t_struct(object):
    __type__ = "struct"

    def __init__(self, name, declaration_list=[]):
        self.name = name
        self.declaration_list = declaration_list


class t_enum(object):
    __type__ = "enum"

    def __init__(self, name, values=[]):
        self.name = name
        self.values = values


class t_namespace(object):
    __type__ = "_t_program__ns"

    def __init__(self, lang, ns):
        self.lang = lang
        self.ns = ns
