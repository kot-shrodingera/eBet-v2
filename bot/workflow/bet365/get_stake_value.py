from typing import Optional

from ...browser import Browser
from ...errors import BotError


stake_value_input_selector = '.bsf-StakeBox_StakeValue-input'

def get_stake_value(browser: Browser) -> Optional[float]:
    stake_value_input = browser.node('Stake Value Input', stake_value_input_selector)
    stake_value_input_text = stake_value_input.get_property('textContent').replace(',', '')

    if stake_value_input_text == '':
        return None
    else:
        try:
            return float(stake_value_input_text)
        except:
            raise BotError(f'Cannot parse current stake: {stake_value_input_text}')
