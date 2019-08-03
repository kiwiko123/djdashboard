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


if __name__ == '__main__':
    checker = WordChecker()
    x = checker.is_word('hello')
    print(x)