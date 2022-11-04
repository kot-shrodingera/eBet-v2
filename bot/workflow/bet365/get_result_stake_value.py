import re
from typing import Optional

from ...browser import Browser
from ...errors import BotError, ErrorType
from ... import logger



result_stake_value_selector = '.bss-StakeBox_StakeValueReceipt'

def get_result_stake_value(browser: Browser) -> float:
    result_stake_value = browser.node('Result Stake Value', result_stake_value_selector, 0)

    result_stake_value_text = result_stake_value.get_property('textContent').replace(',', '')
    result_stake_value_regex = r'^(?:.*?)?(\d+\.\d+)'
    result_stake_value_match = re.search(result_stake_value_regex, result_stake_value_text)
    if not result_stake_value_match:
        raise BotError('Cannot parse result stake value amount', ErrorType.CANNOT_PARSE_RESULT_STAKE_VALUE)
    return float(result_stake_value_match[1])
