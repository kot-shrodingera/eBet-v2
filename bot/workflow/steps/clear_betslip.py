from time import sleep


from .. import Workflow

from ... import logger
from ...errors import BotError, ErrorType


betslip_selector = '.bss-StandardBetslip:not(.bss-StandardBetslip-hidden)'

betslip_single_selector = '.bss-StandardBetslip.bs-AnimationHelper_Single'
betslip_collapsed_selector = '.bss-StandardBetslip.bs-AnimationHelper_Collapsed' # same match
betslip_condensed_selector = '.bss-StandardBetslip.bs-AnimationHelper_Condensed' # different matches

receipt_done_button_selector = '.bss-ReceiptContent_Done'
remove_bet_button_selector = '.bss-RemoveButton'
collapsed_betslip_selector = '.bss-StandardBetslip.bs-AnimationHelper_Collapsed'
expanded_betslip_selector = '.bss-StandardBetslip.bs-AnimationHelper_Expanded'

def is_clear_betslip(self: Workflow) -> bool:
    return not self.browser.node('Betslip Any', betslip_selector, 1, required=False)

def clear_betslip(self: Workflow) -> None:
    after_clear_delay = 0.5
    
    betslip = self.browser.node('Betslip', betslip_selector, 1, required=False)
    if not betslip:
        logger.log('Betslip is empty')
        return
    
    receipt_done_button = self.browser.node('Receipt Done Button', receipt_done_button_selector, 1, required=False)
    if receipt_done_button:
        logger.log(f'Removing bet and waiting {after_clear_delay}s...')
        receipt_done_button.click()
        sleep(after_clear_delay)
        if not is_clear_betslip(self):
            raise BotError('Could not clear receipt done betslip', ErrorType.COULD_NOT_CLEAR_BETSLIP)
        logger.log('Betslip cleared')
        return
    
    betslip_single = self.browser.node('Betslip Single', betslip_single_selector, 1, required=False)
    if betslip_single:
        remove_bet_button = self.browser.node('Remove Bet Button', remove_bet_button_selector, 1)
        logger.log(f'Removing bet and waiting {after_clear_delay}s...')
        remove_bet_button.click()
        sleep(after_clear_delay)
        if not is_clear_betslip(self):
            raise BotError('Could not clear single betslip', ErrorType.COULD_NOT_CLEAR_BETSLIP)
        logger.log('Betslip cleared')
        return
    
    betslip_collapsed = self.browser.node('Betslip Collapsed', betslip_collapsed_selector, 1, required=False)
    if betslip_collapsed:
        logger.log('Expanding collapsed betslip')
        betslip_collapsed.click()
        self.browser.node('Betslip Expanded', expanded_betslip_selector)
        
        while remove_bet_button := self.browser.node('Remove Bet Button', remove_bet_button_selector, 1, required=False):
            logger.log(f'Removing bet and waiting {after_clear_delay}s...')
            remove_bet_button.click()
            sleep(after_clear_delay)
        if not is_clear_betslip(self):
            raise BotError('Could not clear collapsed betslip', ErrorType.COULD_NOT_CLEAR_BETSLIP)
        logger.log('Betslip cleared')
        return
    
    betslip_condensed = self.browser.node('Betslip Condensed', betslip_condensed_selector, 1, required=False)
    if betslip_condensed:
        remove_bet_button = self.browser.node('Remove Bet Button', remove_bet_button_selector, 1)
        logger.log(f'Removing bet and waiting {after_clear_delay}s...')
        remove_bet_button.click()
        sleep(after_clear_delay)
        if not is_clear_betslip(self):
            raise BotError('Could not clear condensed betslip', ErrorType.COULD_NOT_CLEAR_BETSLIP)
        logger.log('Betslip cleared')
        return
    
    raise BotError('Could not clear betslip. Unknown betslip type', ErrorType.COULD_NOT_CLEAR_BETSLIP)
    
