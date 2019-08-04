import pathlib


class WordChecker:
    def __init__(self, path_to_words_file='/usr/share/dict/words'):
        words_file = pathlib.Path(path_to_words_file)
        if not words_file.is_file():
            raise ValueError('"{0}" is not a valid file'.format(path_to_words_file))

        with words_file.open() as infile:
            self._words = {line.strip() for line in infile}


    def is_word(self, word: str) -> bool:
        return word in self._words


    def remove_word(self, word: str) -> None:
        self._words.discard(word)


_CHARACTER_VALUES = {
    'A': 1,
    'B': 2,
    'C': 2,
    'D': 2,
    'E': 1,
    'F': 2,
    'G': 2,
    'H': 2,
    'I': 1,
    'J': 3,
    'K': 3,
    'L': 2,
    'M': 2,
    'N': 2,
    'O': 1,
    'P': 2,
    'Q': 5,
    'R': 2,
    'S': 2,
    'T': 2,
    'U': 1,
    'V': 4,
    'W': 3,
    'X': 5,
    'Y': 4,
    'Z': 5,
}


def get_word_value(word: str) -> int:
    word = word.strip().upper()
    return sum([_CHARACTER_VALUES[c] for c in word if c in _CHARACTER_VALUES])


if __name__ == '__main__':
    checker = WordChecker()
    x = checker.is_word('hello')
    print(x)