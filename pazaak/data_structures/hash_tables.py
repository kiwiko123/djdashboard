import collections
from .containers import BaseContainer


class MultiSet(BaseContainer):

    @property
    def _container(self) -> collections.defaultdict:
        return self.__table

    def __init__(self, iterable=None):
        self.__table = collections.defaultdict(int)
        self._size = 0
        if iterable:
            for item in iterable:
                self.add(item)

    def __str__(self) -> str:
        return '{0}({1})'.format(
            type(self).__name__,
            ', '.join([str(i) for i in self])
        )

    def __repr__(self) -> str:
        result = (i for i in self)
        return '{0}({1})'.format(
            type(self).__name__,
            str(result)
        )

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        for item, count in self._container.items():
            for _ in range(count):
                yield(item)

    def add(self, item) -> None:
        self._container[item] += 1
        self._size += 1

    def discard(self, item) -> None:
        if item in self:
            if self._container[item] > 1:
                self._container[item] -= 1
            else:
                del self._container[item]
            self._size -= 1

    def remove(self, item) -> None:
        if item in self:
            self.discard(item)
        else:
            raise KeyError('"{0}" not in set'.format(item))

    def union(self, other: set) -> 'MultiSet':
        if not (isinstance(other, set) or isinstance(other, MultiSet)):
            raise TypeError('union only takes a set or MultiSet; received {0}'.format(type(other)))

        result = self.copy()
        map(result.add, other)
        return result

    def intersection(self, other: set) -> 'MultiSet':
        if not (isinstance(other, set) or isinstance(other, MultiSet)):
            raise TypeError('intersection only takes a set or MultiSet; received {0}'.format(type(other)))

        return MultiSet((i for i in other if i in self))

    def count(self, item) -> int:
        return self._container[item] if item in self else 0


if __name__ == '__main__':
    pass