from time import sleep

from .. import Workflow

from ... import logger
from ...errors import BotError, ErrorType

bet_credits_checkbox_selector = '.bsc-BetCreditsHeader_Condensed:not(.bsc-BetCreditsHeader_Hide) .bsc-BetCreditsHeader_CheckBox'
bet_credits_checkbox_selected_class = 'bsc-BetCreditsHeader_CheckBox-selected'

def handle_bet_bonuses(self: Workflow):
    bet_credits_checkbox = self.browser.node('Bet Credits Checkbox', bet_credits_checkbox_selector, 1, required=False)
    if bet_credits_checkbox:
        bet_credits_checkbox_class_list = bet_credits_checkbox.get_class_list()
        if bet_credits_checkbox_class_list is None:
            raise BotError('Cannot get Bet Credits Checkbox class list', ErrorType.CANNOT_HANDLE_BET_CREDITS)
        
        bet_credits_selected = bet_credits_checkbox_selected_class in bet_credits_checkbox_class_list
        
        if self.settings.use_bet_credits:
            if bet_credits_selected:
                logger.log('Bet Credits already selected')
            else:
                logger.log('Bet Credits not selected. Clicking')
                bet_credits_checkbox.click()
                sleep(0.5) # animations
        else:
            if bet_credits_selected:
                logger.log('Bet Credits selected. Clicking')
                bet_credits_checkbox.click()
                sleep(0.5) # animations
            else:
                logger.log('Bet Credits not selected')