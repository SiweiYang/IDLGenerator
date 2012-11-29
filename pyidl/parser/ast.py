

class t_struct(object):

    def __init__(self, name, declaration_list=[]):
        self.name = name
        self.declaration_list = declaration_list


class t_enum(object):

    def __init__(self, name, values=[]):
        self.name = name
        self.values = values
