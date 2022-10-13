from enum import Enum
from typing import Dict, Union

class ErrorType(Enum):
    UNKNOWN = 1
    WRONG_BET_OPENED = 2

class BotError(Exception):
    message: str
    error_type: ErrorType
    data: Union[Dict, None]
    
    def __init__(self, message: str, type: ErrorType = ErrorType.UNKNOWN, data: Union[Dict, None] = None):
        self.message = message
        super().__init__(self.message)
        self.type = type
        self.data = data
