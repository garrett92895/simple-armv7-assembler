from . import tokentype

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    @classmethod
    def fromChildren(cls, token_type, *args):
        return cls(token_type, args)

    def __str__(self):
        return str(str(tokentype.types[self.token_type]) + " | " + str(self.value))

    def __repr__(self):
        return "{" + self.__str__() + "}"

    def __eq___(self, comparison_object):
        if self.token_type == tokentype.NullType and comparison_object is None:
            return True
        else:
            return super.__eq__(comparison_obect)
