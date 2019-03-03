import datetime
from commutity import helper

class LoginInfo:
    def __init__(self, username: str):
        self._username = username 
        self._time_in = datetime.datetime.now()
        self._time_out = None

    def __str__(self) -> str:
        return helper.generic_obj_str(self, 'username', 'time_in', 'time_out')
        
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def time_in(self) -> datetime.datetime:
        return self._time_in
    
    @property
    def time_out(self) -> datetime.datetime:
        return self._time_out
    
    def log_out(self) -> None:
        self._time_out = datetime.datetime.now()