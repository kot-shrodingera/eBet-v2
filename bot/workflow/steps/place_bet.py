from datetime import datetime
from time import sleep

from .check_bet import check_bet
from .after_successful_bet import after_successful_bet

from .. import Workflow, bet365

from ... import logger


place_bet_button_selector = '.bsf-PlaceBetButton:not(.Hidden), .bsf-AcceptButton:not(.Hidden)'
receipt_done_button_selector = '.bss-ReceiptContent_Done'

def place_bet(self: Workflow) -> bool:
    logger.log('Placing Bet')
    self.place_bet_start = datetime.now()
    place_bet_button = self.browser.node('Place Bet Button', place_bet_button_selector)
    place_bet_button.click()

    # TODO: add tries limit
    while (place_bet_result := bet365.get_place_bet_result(self.browser)) == 'Odds Changed':
        logger.log('Odds Changed. Retrying')

        check_bet(self)

        place_bet_button = self.browser.node('Place Bet Button', place_bet_button_selector)
        place_bet_button.click()
        sleep(0.5) # For last "Odds Changed" message to disappear

    if place_bet_result == 'Bet Placed':
        logger.log(place_bet_result)
        after_successful_bet(self)
        sleep(0.5) # animations
        receipt_done_button = self.browser.node('Receipt Done Button', receipt_done_button_selector)
        receipt_done_button.click()
        sleep(0.5) # animations
        logger.log('Returning to My Bets')
        self.browser.go_to_url(self.bet365_my_bets_url)
        return True
    
    if place_bet_result == 'Check My Bets':
        pass
    
    if place_bet_result == 'Logout':
        pass

    logger.log(place_bet_result)
    return False
