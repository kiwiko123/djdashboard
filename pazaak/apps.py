import pathlib

from django.apps import AppConfig
from server.serialization import EnumSerializer

_ENUM_WRITE_FILE = 'react/src/pazaak/js/enums.js'

class PazaakConfig(AppConfig):
    name = 'pazaak'

    def ready(self):
        enum_serializer = EnumSerializer(_ENUM_WRITE_FILE)
        enum_serializer.export()