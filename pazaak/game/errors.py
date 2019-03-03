

class _PazaakGameError(Exception):
    pass

class GameOverError(_PazaakGameError):
    pass

class GameLogicError(_PazaakGameError):
    pass