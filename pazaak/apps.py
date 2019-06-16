import pathlib

from django.apps import AppConfig
from pazaak.enums import export_enums_to_js

_ENUM_WRITE_FILE = 'react/src/pazaak/js/enums.js'

class PazaakConfig(AppConfig):
    name = 'pazaak'

    def ready(self):
        """
        The contents of this method fire on server startup.
        Exports the specified Serializable enum classes to JS.
        """
        write_file = pathlib.Path(_ENUM_WRITE_FILE)
        export_enums_to_js(write_file)