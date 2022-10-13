from time import sleep

from ..bet365.get_balance import get_balance
from ..bet365.get_stake_value import get_stake_value
from .. import Workflow

from ... import logger
from ...errors import BotError, ErrorType


stake_value_input_empty_selector = '.bsf-StakeBox_StakeValue-input.bsf-StakeBox_StakeValue-empty'
stake_value_input_units_selector = '.bsf-StakeBox_StakeUnits'
remember_stake_value_button_selector = '.bsf-RememberStakeButtonNonTouch'
remember_stake_value_button_hit_area_selector = '.bsf-RememberStakeButtonNonTouch_HitArea'

remember_stake_value_button_active_class = 'bsf-RememberStakeButtonNonTouch-active'

def set_stake_value(self: Workflow) -> None:
    remember_stake_value_button = self.browser.node('Remember Stake Value Button', remember_stake_value_button_selector)
    
    remember_stake_value_button_class_list = remember_stake_value_button.get_class_list()

    if remember_stake_value_button_class_list and remember_stake_value_button_active_class not in remember_stake_value_button_class_list:
        # logger.log('Remember Stake Value Button is not active')
        pass
    else:
        logger.log('Deactivating Remember Stake Value Button')
        remember_stake_value_button_hit_area = self.browser.node('Remember Stake Value Button Hit Area', remember_stake_value_button_hit_area_selector)
        remember_stake_value_button_hit_area.click()
    
    
    stake_value = get_stake_value(self.browser)
    if stake_value is None:
        logger.log('Current stake value is empty')
        stake_value_input_empty = self.browser.node('Stake Value Input Empty', stake_value_input_empty_selector)
        stake_value_input_empty.click()
    else:
        if stake_value == self.target_stake_value:
            logger.log('Stake Value is already set')
            return
        logger.log(f'Current stake: {stake_value}. Clearing')
        stake_value_input_units = self.browser.node('Stake Value Input Units', stake_value_input_units_selector)
        stake_value_input_units.click()
        sleep(0.1)
    
    self.browser.crdi.send('0') # pyright: reportUnknownMemberType=false
    sleep(0.1)
    stake_value = get_stake_value(self.browser)
    if stake_value != 0:
        raise BotError(f'Could not clear stake value ({stake_value})', ErrorType.COULD_NOT_CLEAR_STAKE_VALUE)
    
    self.browser.crdi.send(str(self.target_stake_value)) # pyright: reportUnknownMemberType=false
    sleep(0.1)
    stake_value = get_stake_value(self.browser)
    if stake_value != self.target_stake_value:
        raise BotError(f'Could not set stake value ({stake_value})', ErrorType.COULD_NOT_SET_STAKE_VALUE)


