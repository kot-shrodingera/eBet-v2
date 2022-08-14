from time import sleep
from datetime import datetime

from .. import Workflow, bet365

from ... import logger
from ...browser import Node
from ...errors import BotError


market_opened_class = 'sip-MarketGroup_Open'
betslip_selector = '.bs-AnimationHelper_ContainerNoScale'

def open_selection(self: Workflow) -> None:
    logger.log(f'Opening Selection {self.bet_details["market"]}|{self.bet_details["column"]}|{self.bet_details["selection"]}')
    selection_button = None
    find_try = 0
    tries_limit = 20
    
    while not isinstance(market_title := bet365.get_market_title(self.browser, self.bet_details['market']), Node):
        find_try += 1
        logger.log(market_title)
        logger.log(f'Try №{find_try} of {tries_limit}')
        if find_try >= tries_limit:
            break
        sleep(0.5)
        
    if not isinstance(market_title, Node):
        raise BotError('Market Title not found')
    logger.log('Market Title found')
    
    if market_opened_class not in market_title.get_class_list():
        logger.log('Market Title is not opened. Opening')
        market_title_text = bet365.get_market_title_text(self.browser, self.bet_details['market'])
        if isinstance(market_title_text, str):
            raise BotError(market_title_text)
        market_title_text.click()
        sleep(0.1) # animations
    else:
        logger.log('Market is openned')
    
    while not isinstance(selection_button := bet365.get_selection_button(self.browser, self.bet_details['market'], self.bet_details['column'], self.bet_details['selection']), Node):
        find_try += 1
        logger.log(f'{selection_button}. Try №{find_try} of {tries_limit}')
        if find_try >= tries_limit:
            break
        sleep(0.5)
        
    if not isinstance(selection_button, Node):
        raise BotError('Selection Button not found')
    logger.log('Selection Button found')
        
    if 'Suspended' in selection_button.get_class_list():
        raise BotError('Selection is Suspended')
    
    if self.settings.placed_bet_to_open_delay is not None and self.bet_placed_time:
        timedelta = datetime.now() - self.bet_placed_time
        delay = self.settings.placed_bet_to_open_delay - timedelta.seconds + timedelta.microseconds / 1000000
        if delay > 0:
            logger.log(f'Placed Bet to Open delay: {delay:.2f} seconds')
            sleep(delay)
    
    selection_button.click()

    self.browser.node('Betslip', betslip_selector, not_found_error='Betslip not opened')
