import collections
from data_structures.matrices.matrix import Matrix


class _Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return '_Coordinate({0}, {1})'.format(self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def _make_coordinate(x: int, y: int):
    return _Coordinate(x, y)


class DictMatrix(Matrix):
    """
    A matrix whose underlying data structure is a dictionary.
    Compared to ListMatrix, many of the matrix operations are significantly more expensive in terms of time complexity.
    For example, there is no easy way of obtaining a given row without iterating through all entries in the dictionary.
    However, a DictMatrix only takes up as much space as their are items within it.
    A ListMatrix must have a predetermined rectangular shape, and will often take up much more space than is actually needed.
    As such, DictMatrix is the more scalable option.
    """
    def __init__(self):
        self._matrix = {}


    def __len__(self) -> int:
        return len(self._matrix)


    def __bool__(self) -> bool:
        return len(self) > 0


    def __delitem__(self, key: (int, int)) -> None:
        self._verify_coordinate_argument(key)
        x = key[0]
        if x in self._matrix:
            del self._matrix[x]


    def get_value(self, row: int, column: int):
        self._validate_row_index(row)
        self._validate_column_index(column)
        coordinate = _make_coordinate(row, column)
        return self._matrix[coordinate]


    def set_value(self, row: int, column: int, value):
        self._validate_row_index(row)
        self._validate_column_index(column)
        coordinate = _make_coordinate(row, column)
        self._matrix[coordinate] = value


    def rows(self) -> [list]:
        row_indices = sorted({row for row, _ in self._matrix})
        return [self.row(row) for row in row_indices]


    def row(self, row_index: int) -> list:
        dataholder = collections.namedtuple('Info', ('column', 'value'))
        values_in_row = [dataholder(coordinate.y, value) for coordinate, value in self._matrix.items() if coordinate.x == row_index]
        values_in_row.sort(key=lambda info: info.column)
        return [info.value for info in values_in_row]


    def column(self, column_index: int) -> list:
        dataholder = collections.namedtuple('Info', ('row', 'value'))
        values_in_column = [dataholder(coordinate.x, value) for coordinate, value in self._matrix.items() if coordinate.y == column_index]
        values_in_column.sort(key=lambda info: info.row)
        return [info.value for info in values_in_column]


    def row_count(self) -> int:
        return len(self.rows())


    def column_count(self) -> int:
        return len({column for _, column in self._matrix})


    def is_blank(self, row: int, column: int) -> bool:
        return _make_coordinate(row, column) not in self._matrix



if __name__ == '__main__':
    m = DictMatrix()
    a = _make_coordinate(1, 2)
    b = _make_coordinate(1, 3)
    c = _make_coordinate(3, 5)
    d = _make_coordinate(3, 4)

    m._matrix[a] = 'a'
    m._matrix[b] = 'b'
    m._matrix[c] = 'c'
    m._matrix[d] = 'd'

    print(m.column(5))