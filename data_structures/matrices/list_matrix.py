from data_structures.matrices.matrix import Matrix


def _create_matrix(n_rows: int, n_cols: int, initializer: callable) -> [list]:
    return [[initializer()] * n_cols for _ in range(n_rows)]


class ListMatrix(Matrix):
    def __init__(self, number_of_rows: int, number_of_columns: int, initializer=lambda: None):
        self._matrix = _create_matrix(number_of_rows, number_of_columns, initializer)
        self._column_count = number_of_columns


    def __str__(self) -> str:
        return 'ListMatrix({0})'.format(self._matrix)


    def get_value(self, row: int, column: int):
        self._validate_row_index(row)
        self._validate_column_index(column)
        return self._matrix[row][column]


    def set_value(self, row: int, column: int, value) -> None:
        """
        Use bracket-notation ([]) to set the value at a specific (row, column) coordinate in the matrix.
        Must provide exactly two (row, column) integers, which are expected to be zero-indexed.
        Example:
        >> matrix[0, 1] = 'A'
        >> # sets the position in the 0th row, 1st column to 'A'
        """
        self._validate_row_index(row)
        self._validate_column_index(column)
        self._matrix[row][column] = value


    def rows(self) -> list:
        return list(self._matrix)


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



if __name__ == '__main__':
    matrix = ListMatrix(4, 4)
    matrix.print()