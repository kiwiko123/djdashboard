import abc


class _Blank:
    def __init__(self):
        self._placeholder = 'O'

    def __str__(self) -> str:
        return self._placeholder


def _create_matrix(n_rows: int, n_cols: int, initializer: callable) -> [list]:
    return [[initializer()] * n_cols for _ in range(n_rows)]


class ListMatrix:
    def __init__(self, number_of_rows: int, number_of_columns: int, initializer=lambda: _Blank()):
        self._matrix = _create_matrix(number_of_rows, number_of_columns, initializer)
        self._column_count = number_of_columns
        self._empty_cell_count = self.total_cells()
        self._initializer = initializer


    def __str__(self) -> str:
        return 'ListMatrix({0})'.format(self._matrix)


    def __getitem__(self, index) -> list:
        """
        Returns a copy of the row at the given index.
        """
        if type(index) is int:
            self._validate_row_index(index)
            return self.row(index)
        elif type(index) is tuple and len(index) == 2:
            row, column = index
            self._validate_row_index(row)
            self._validate_column_index(column)
            return self._matrix[row][column]
        else:
            raise ValueError('Expected 1-2 integer indices; received "{0}"'.format(index))


    def __setitem__(self, key, value) -> None:
        """
        Use bracket-notation ([]) to set the value at a specific (row, column) coordinate in the matrix.
        Must provide exactly two (row, column) integers, which are expected to be zero-indexed.
        Example:
        >> matrix[0, 1] = 'A'
        >> # sets the position in the 0th row, 1st column to 'A'
        """
        if not (type(key) is tuple):
            raise ValueError('Expected 2 values as the index/key; received {0}'.format(key))
        if len(key) != 2:
            raise ValueError('Expected exactly 2 values as the index; received {0}'.format(len(key)))

        row, column = key
        self._validate_row_index(row)
        self._validate_column_index(column)
        self._matrix[row][column] = value

        if value == self._blank:
            counter = -1 if self._occupied_cells else 0
        else:
            counter = 1

        self._occupied_cells += counter


    def print(self) -> None:
        """
        Prints the matrix in a readable format.
        """
        for row in self.rows():
            for col in row:
                print(col, end=' ')
            print()


    def all_values(self) -> iter:
        for row in self.rows():
            yield from row


    def _validate_row_index(self, n: int) -> None:
        if not (0 <= n < self.row_count()):
            raise IndexError('Row index {0} is out-of-bounds'.format(n))


    def _validate_column_index(self, n: int) -> None:
        if not (0 <= n < self.column_count()):
            raise IndexError('Column index {0} is out-of-bounds'.format(n))


    def total_cells(self) -> int:
        return self.row_count() * self.column_count()


    def occupied_cells(self) -> int:
        return self._occupied_cells


    def empty_cells(self) -> int:
        return self.total_cells() - self.occupied_cells()


    def rows(self) -> list:
        return self._matrix


    def row(self, row_index: int) -> list:
        self._validate_row_index(row_index)
        return list(self._matrix[row_index])


    def column(self, column_index: int) -> list:
        self._validate_column_index(column_index)
        return [row[column_index] for row in self.rows()]


    def row_count(self) -> int:
        return len(self.rows())


    def column_count(self) -> int:
        return self._column_count


    def is_blank(self, row: int, column: int) -> bool:
        return self[row, column] == self._initializer()



if __name__ == '__main__':
    matrix = ListMatrix(4, 4)
    matrix.print()