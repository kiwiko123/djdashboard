import enum
import pathlib

from django.apps import AppConfig
from pazaak.game.status import GameStatus


_ENUMS_TO_SERIALIZE = [GameStatus]
_ENUM_WRITE_FILE = 'pazaak/react/src/js/enums.js'

class PazaakConfig(AppConfig):
    name = 'pazaak'

    def ready(self):
        write_file = pathlib.Path(_ENUM_WRITE_FILE)
        export_enums_to_js(_ENUMS_TO_SERIALIZE, write_file)


def export_enums_to_js(enums: [enum.Enum], write_file: pathlib.Path):
    with write_file.open('w') as outfile:
        header = [
            '// =========================',
            '// || AUTO-GENERATED FILE ||',
            '// ========================='
        ]

        outfile.write('\n'.join(header))
        outfile.write('\n\n')

        for enum_class in _ENUMS_TO_SERIALIZE:
            enum_class.write_to_js(outfile)
            outfile.write('\n')