import pathlib

from django.apps import AppConfig
from pazaak.enums import export_enums_to_js

_ENUM_WRITE_FILE = 'pazaak/react/src/js/enums.js'

class PazaakConfig(AppConfig):
    name = 'pazaak'

    def ready(self):
        write_file = pathlib.Path(_ENUM_WRITE_FILE)
        export_enums_to_js(write_file)