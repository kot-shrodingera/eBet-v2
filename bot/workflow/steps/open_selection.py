from time import sleep
from datetime import datetime

from .. import Workflow, bet365

from ... import logger
from ...errors import BotError


betslip_selector = '.bs-AnimationHelper_ContainerNoScale'

def open_selection(self: Workflow) -> None:
    logger.log(f'Opening Selection {self.bet_details["market"]}|{self.bet_details["column"]}|{self.bet_details["selection"]}')
    selection_button = None
    find_try = 0
    tries_limit = 10
    while not (selection_button := bet365.get_selection_button(self.browser, self.bet_details['market'], self.bet_details['column'], self.bet_details['selection'])):
        find_try += 1
        logger.log(f'Selection Buton not found. Try №{find_try} of {tries_limit}')
        if find_try >= tries_limit:
            break
        sleep(0.5)
        
    if not selection_button:
        raise BotError('Selection Button not found')
    selection_button = self.browser.node('Selection Button', remote_object_id=selection_button)
    
    if self.settings.placed_bet_to_open_delay is not None and self.bet_placed_time:
        timedelta = datetime.now() - self.bet_placed_time
        delay = self.settings.placed_bet_to_open_delay - timedelta.seconds + timedelta.microseconds / 1000000
        if delay > 0:
            logger.log(f'Placed Bet to Open delay: {delay:.2f} seconds')
            sleep(delay)
    
    selection_button.click()

    self.browser.node('Betslip', betslip_selector, not_found_error='Betslip not opened')
