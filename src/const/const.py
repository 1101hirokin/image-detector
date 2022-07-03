from exceptions import exceptions

class _const:

  def __setattr__(self, name: str, __value) -> None:
    if name in self.__dict__:
      raise exceptions.ConstError("Can't rebind const (%s)" % name)
    self.__dict__[name] = __value

import sys
sys.modules[__name__] = _const()