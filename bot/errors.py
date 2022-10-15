from enum import Enum
from typing import Dict, Optional

class ErrorType(Enum):
    UNKNOWN = 1
    UNCAUGHT_EXCEPTION = 2
    CHROME_DIED = 3
    JS_EXCEPTION = 100
    CANNOT_GET_JS_FUNCTION_RESULT = 101
    SOME_ELEMENT_NOT_FOUND = 102
    UNKNOWN_STAKE_TYPE_IN_SETTINGS = 120
    PAUSE_ON_POREZ = 150
    BETS_REQUEST_TIMEOUT = 201
    BETS_REQUEST_INVALID_JSON = 202
    BETS_REQUEST_NO_DATA_FORKS = 203
    CANNOT_PARSE_SELECTION_DETAILS = 204
    NO_DATA_IN_BET_DETAILS = 205
    WRONG_DATA_IN_BET_DETAILS = 206
    CANNOT_PARSE_CURRENCY = 300
    CANNOT_PARSE_BALANCE = 301
    CANNOT_PARSE_PARAMETER = 302
    CANNOT_PARSE_SCORE = 302
    SELECTION_NOT_FOUND = 400
    SELECTION_IS_SUSPENDED = 401
    WRONG_BET_OPENED = 402
    BETSLIP_DID_NOT_OPENED = 403
    COULD_NOT_CLEAR_STAKE_VALUE = 404
    COULD_NOT_SET_STAKE_VALUE = 405
    STAKE_IS_HIGHER_THAN_BALANCE = 500
    COEFFICIENT_IS_LOWER_THAN_MINIMUM = 501
    COEFFICIENT_IS_HIGHER_THAN_MAXIMUM = 502
    PARAMETER_HAS_CHANGED = 503
    NOT_TARGET_SCORE = 504
    ACCOUNT_RESTRICTED = 600

class BotError(Exception):
    message: str
    type: ErrorType
    data: Optional[Dict]
    
    def __init__(self, message: str, type: ErrorType = ErrorType.UNKNOWN, data: Optional[Dict] = None):
        self.message = message
        super().__init__(self.message)
        self.type = type
        self.data = data
