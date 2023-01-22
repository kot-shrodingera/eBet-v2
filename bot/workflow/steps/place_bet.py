from datetime import datetime
from time import sleep

from .. import Workflow, steps, bet365

from ... import logger
from ...errors import BotError, ErrorType


place_bet_button_selector = '.bsf-PlaceBetButton:not(.Hidden), .bsf-AcceptButton:not(.Hidden)'
place_bet_refer_button_selector = '.bsf-PlaceBetReferButton:not(.Hidden)'
receipt_done_button_selector = '.bss-ReceiptContent_Done'

def place_bet(self: Workflow) -> None:
    logger.log('Placing Bet')
    
    place_try = 0
    place_tries_limit = 5 # TODO: set limit in settings

    if self.settings.placed_bet_to_place_delay is not None and self.bet_placed_time:
        timedelta = datetime.now() - self.bet_placed_time
        delay = self.settings.placed_bet_to_place_delay - timedelta.seconds + timedelta.microseconds / 1000000
        if delay > 0:
            logger.log(f'Placed Bet to Place delay: {delay:.2f} seconds')
            sleep(delay)
            
    place_bet_result = 'No tries'

    while place_try < place_tries_limit:
        place_try += 1
        logger.log(f'Place Try №{place_try} of {place_tries_limit}')

        steps.check_bet(self)

        self.place_bet_start = datetime.now()
        place_bet_button = self.browser.node('Place Bet Button', place_bet_button_selector)
        place_bet_button.click()
        sleep(0.5) # For last messages to disappear
        
        place_bet_result = bet365.get_place_bet_result(self.browser)

        if place_bet_result == 'Bet Placed':
            logger.log('Bet Placed')
            self.traders_accepted_amount = None
            steps.after_successful_bet(self)
            sleep(0.5) # animations
            receipt_done_button = self.browser.node('Receipt Done Button', receipt_done_button_selector)
            receipt_done_button.click()
            sleep(0.5) # animations
            if self.settings.close_page_on_placed_bet:
                self.browser.go_to_url('chrome://newtab')
            logger.log('Returning to My Bets')
            self.browser.go_to_url(self.bet365_my_bets_url)
            return
        
        if place_bet_result == 'Odds Changed':
            logger.log('Odds Changed. Retrying')
            continue
        
        if place_bet_result == 'Traders':
            logger.log('Traders. Applying')
            place_bet_refer_button = self.browser.node('Place Bet Refer Button', place_bet_refer_button_selector)
            place_bet_refer_button.click()
            sleep(0.5) # For last messages to disappear
            
            place_bet_traiders = bet365.get_place_bet_traders_result(self.browser)
            if not place_bet_traiders:
                raise BotError('Place Bet Traiders Fail', ErrorType.PLACE_BET_TRAIDERS_FAILED)
            
            self.traders_accepted_amount = bet365.get_traders_accepted_amount(self.browser)
            steps.after_successful_bet(self)
            sleep(0.5) # animations
            receipt_done_button = self.browser.node('Receipt Done Button', receipt_done_button_selector)
            receipt_done_button.click()
            sleep(0.5) # animations
            if self.settings.close_page_on_placed_bet:
                self.browser.go_to_url('chrome://newtab')
            logger.log('Returning to My Bets')
            self.browser.go_to_url(self.bet365_my_bets_url)
            return
        
        if place_bet_result == 'Account Restricted':
            self.restrict = True
            raise BotError('Account Restricted', ErrorType.ACCOUNT_RESTRICTED)
        
        if place_bet_result == 'Check My Bets':
            raise BotError('Check My Bets', ErrorType.CHECK_MY_BETS)
        
        if place_bet_result == 'Logout':
            raise BotError('Logout', ErrorType.PLACE_BET_LOGOUT)

        logger.log(place_bet_result)

    raise BotError(f'Place Bet Fail (last try result: {place_bet_result})', ErrorType.PLACE_BET_FAILED)
