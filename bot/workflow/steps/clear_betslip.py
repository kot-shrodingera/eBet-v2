from time import sleep


from .. import Workflow

from ... import logger
from ...errors import BotError, ErrorType



bet_count_selector = '.bss-DefaultContent_BetCount'
clear_betslip_button_selector = '.bss-RemoveButton, .bss-ReceiptContent_Done'
collapsed_betslip_selector = '.bss-StandardBetslip.bs-AnimationHelper_Collapsed'
expanded_betslip_selector = '.bss-StandardBetslip.bs-AnimationHelper_Expanded'
remove_bet_button_selector = '.bss-RemoveButton'

def clear_betslip(self: Workflow) -> None:
    after_clear_delay = 0.5
    bet_count = self.browser.node('Bet Count', bet_count_selector, 1)
    bet_count_int = int(bet_count.get_property('textContent'))
    logger.log(f'Bet count: {bet_count_int}')
    
    if bet_count_int == 0:
        logger.log('Betslip is empty')
        return
    
    clear_betslip_button = self.browser.node('Clear Betslip Button', clear_betslip_button_selector, 1, required=False)
    if clear_betslip_button and clear_betslip_button.is_visible():
        logger.log(f'Clearing Betslip and waiting {after_clear_delay}s...')
        clear_betslip_button.click()
        sleep(after_clear_delay)
        return

    logger.log('No clear betslip button. Maybe collapsed betslip')
    collapsed_betslip = self.browser.node('Collapsed Betslip', collapsed_betslip_selector, 1)
    logger.log('Expanding collapsed betslip')
    collapsed_betslip.click()
    self.browser.node('Expanded Betslip', expanded_betslip_selector)
    
    while remove_bet_button := self.browser.node('Remove Bet Button', remove_bet_button_selector, 1, required=False):
        logger.log(f'Removing bet and waiting {after_clear_delay}s...')
        remove_bet_button.click()
        sleep(after_clear_delay)
    
    if float(bet_count.get_property('textContent')) != 0:
        raise BotError('Could not clear betslip', ErrorType.COULD_NOT_CLEAR_BETSLIP)
    
    logger.log('Betslip is cleared')
