from types import MethodType

def dirty_property(real_var, if_dirty, to_dirty=None, to_update=None):

    if not to_dirty:
        to_dirty = []
    if not to_update:
        to_update = []

    def fget(self):
        v = self.__getattribute__(real_var)
        if v == None:
            v = if_dirty(self)
            self.__setattr__(real_var, v)
        return v

    def fset(self, value):
        self.__setattr__(real_var, value)
        for attr in to_update:
            # This will update partner values
            self.__getattribute__(attr)
        for dirt in to_dirty:
            self.__setattr__(dirt, None)

    return property(fget, fset)


class Effect(object):

    def __init__(self, engine):
        self.engine = engine

    def apply(self, target):
        self.target = target
        self.orig_tick = target.tick
        target.tick = MethodType(self.monkey_patch(target), target, target.__class__)

    def monkey_patch(self, target):

        def new_tick(monkey_self, *args, **kwargs):
            self.tick(self, monkey_self, *args, **kwargs)

        return new_tick


def flatten(li):
    """
    Given a list, potentially containing other lists, flatten the list.

    >>> flatten([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> flatten([1, [2, 3], 4])
    [1, 2, 3, 4]
    >>> flatten([[1, 2], [3, [4]]])
    [1, 2, 3, 4]
    >>> flatten([1, [2, [3, [4]]]])
    [1, 2, 3, 4]
    """
    flattened = []
    try:
        for o in li:
            flattened.extend(flatten(o))
    except TypeError:
        return [li]

    return flattened


if __name__ == '__main__':
    import doctest
    doctest.testmod()
