

class _PazaakError(Exception):
    pass

class GameOverError(_PazaakError):
    pass

class GameLogicError(_PazaakError):
    pass

class ServerError(_PazaakError):
    pass

class DataError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass