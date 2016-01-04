# -*- coding: utf-8 -*-

import sys

class _const:
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, key, value):
        if self.__dict__.get(key):
            raise(self.ConstError, u"can't change const. {0}".format(key))
        if not key.isupper():
            raise (self.ConstCaseError, "const name '{0}' is not all uppercase".format(key))
        self.__dict__[key] = value

sys.modules[__name__] = _const()