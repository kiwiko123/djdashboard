

class ImmutableDict(dict):
    def __init__(self, dictionary=None, **kwargs):
        self._can_mutate = True
        super().__init__(dictionary, **kwargs)
        self._can_mutate = False

    def __setattr__(self, key, value) -> None:
        whitelist = {'_can_mutate'}

        if key in whitelist:
            if (not hasattr(self, key)) or self._can_mutate:
                super().__setattr__(key, value)
        else:
            raise ValueError('Cannot mutate an immutable object')


if __name__ == '__main__':
    f = {'a': 10, 'b': 20, 'c': 30}
    x = ImmutableDict(f)
    print(x)
    x['a'] = 100
    print(x)