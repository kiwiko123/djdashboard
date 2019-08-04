import abc


class _Blank:
    def __init__(self):
        self._placeholder = '-'

    def __str__(self) -> str:
        return self._placeholder


class Matrix(metaclass=abc.ABCMeta):

    @staticmethod
    def get_placeholder():
        return _Blank()


    def __getitem__(self, key: int or (int, int)):
        if type(key) is int:
            return self.row(key)
        elif type(key) is tuple and len(key) == 2:
            row, column = key
            return self.get_value(row, column)

        raise ValueError('Expected 1-2 integer indices; received "{0}"'.format(key))


    def __setitem__(self, key: (int, int), value):
        self._verify_coordinate_argument(key)
        x, y = key
        self.set_value(x, y, value)


    def __delitem__(self, key: (int, int)) -> None:
        self._verify_coordinate_argument(key)
        x, y = key
        self[x, y] = self.get_placeholder()


    def __contains__(self, coordinate: (int, int)) -> bool:
        x, y = coordinate
        return not self.is_blank(x, y)


    @abc.abstractmethod
    def get_value(self, row: int, column: int):
        pass


    @abc.abstractmethod
    def set_value(self, row: int, column: int, value) -> None:
        pass


    @abc.abstractmethod
    def rows(self) -> [list]:
        pass


    @abc.abstractmethod
    def row(self, row_index: int) -> list:
        pass


    def column(self, column_index: int) -> list:
        self._validate_column_index(column_index)
        return [row[column_index] for row in self.rows()]


    def row_count(self) -> int:
        return len(self.rows())


    @abc.abstractmethod
    def column_count(self) -> int:
        pass


    def print(self) -> None:
        """
        Prints the matrix in a readable format.
        """
        for row in self.rows():
            for col in row:
                print(col, end=' ')
            print()


    def total_cells(self) -> int:
        return self.row_count() * self.column_count()


    def all_values(self) -> iter:
        for row in self.rows():
            yield from row


    def is_blank(self, row: int, column: int) -> bool:
        return self[row, column] != self.get_placeholder()


    def _validate_row_index(self, n: int) -> None:
        if not (0 <= n < self.row_count()):
            raise IndexError('Row index {0} is out-of-bounds'.format(n))


    def _validate_column_index(self, n: int) -> None:
        if not (0 <= n < self.column_count()):
            raise IndexError('Column index {0} is out-of-bounds'.format(n))


    @staticmethod
    def _verify_coordinate_argument(key: (int, int)) -> None:
        if not (type(key) is tuple):
            raise ValueError('Expected 2 values as the index/key; received {0}'.format(key))
        if len(key) != 2:
            raise ValueError('Expected exactly 2 values as the index; received {0}'.format(len(key)))