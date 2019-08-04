from django.apps import AppConfig
from server.serialization import EnumSerializer
from scrabble import enums


_ENUM_WRITE_FILE = 'react/src/scrabble/js/enums.js'


class ScrabbleConfig(AppConfig):
    name = 'scrabble'

    def ready(self):
        enum_serializer = EnumSerializer(_ENUM_WRITE_FILE, enums)
        enum_serializer.export()
