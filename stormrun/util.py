def dirty_property(real_var, if_dirty, to_dirty=None):

    if not to_dirty:
        to_dirty = []

    def fget(self):
        v = self.__getattribute__(real_var)
        if v == None:
            v = if_dirty(self)
            self.__setattr__(real_var, v)
        return v

    def fset(self, value):
        self.__setattr__(real_var, value)
        for dirt in to_dirty:
            self.__setattr__(dirt, None)

    return property(fget, fset)
