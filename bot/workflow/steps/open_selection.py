from time import sleep
from datetime import datetime

from .. import steps

from .. import Workflow, bet365

from ... import logger
from ...browser import Node
from ...errors import BotError, ErrorType


market_opened_class = 'sip-MarketGroup_Open'
betslip_selector = '.bs-AnimationHelper_ContainerNoScale'

def open_selection(self: Workflow) -> None:
    open_try = 0
    last_error: BotError = BotError('Unknown Open Selection Error') # Will always be redefined?
    
    while open_try < self.settings.open_tries_limit:
        open_try += 1
        logger.log(f'Open Try №{open_try} of {self.settings.open_tries_limit}')
        try:
            logger.log(f'Opening Selection {self.bet_details["market"]}|{self.bet_details["column"]}|{self.bet_details["selection"]}')
            selection_button = None
            find_try = 0
            
            while find_try < self.settings.find_tries_limit:
                find_try += 1
                if find_try > 1:
                    sleep(0.2)
                logger.log(f'Find Try №{find_try} of {self.settings.find_tries_limit}')
                
                market_title = bet365.get_market_title(self.browser, self.bet_details['market'])
                if not isinstance(market_title, Node) and not isinstance(market_title, str):
                    raise BotError('Get market title js function wrong return type', ErrorType.CANNOT_GET_JS_FUNCTION_RESULT)
                logger.log(f'Searching for market {self.bet_details["market"]}')
                if not isinstance(market_title, Node):
                    if find_try == self.settings.find_tries_limit:
                        logger.log(market_title)
                    continue
                logger.log('Market Title found')
            
                class_list = market_title.get_class_list()
                if class_list and market_opened_class not in class_list:
                    logger.log('Market Title is not opened. Opening')
                    market_title_text = bet365.get_market_title_text(self.browser, self.bet_details['market'])
                    if not isinstance(market_title_text, Node) and not isinstance(market_title_text, str):
                        raise BotError('Get market title text js function wrong return type', ErrorType.CANNOT_GET_JS_FUNCTION_RESULT)
                    if not isinstance(market_title_text, Node):
                        logger.log(market_title_text)
                        continue
                    market_title_text.click()
                    sleep(0.1)
                    continue
                logger.log('Market is openned')
                
                selection_button = bet365.get_selection_button(self.browser, self.bet_details['market'], self.bet_details['column'], self.bet_details['selection'])
                if not isinstance(selection_button, Node) and not isinstance(selection_button, str):
                    raise BotError('Get selection button js function wrong return type', ErrorType.CANNOT_GET_JS_FUNCTION_RESULT)
                if not isinstance(selection_button, Node):
                    logger.log(selection_button)
                    continue
                logger.log('Selection found')
                break
            if not isinstance(selection_button, Node):
                raise BotError('Selection not found', ErrorType.SELECTION_NOT_FOUND)
            
            class_list = selection_button.get_class_list()
            if class_list and 'Suspended' in class_list:
                raise BotError('Selection is Suspended', ErrorType.SELECTION_IS_SUSPENDED)
                
            if self.settings.placed_bet_to_open_delay is not None and self.bet_placed_time:
                timedelta = datetime.now() - self.bet_placed_time
                delay = self.settings.placed_bet_to_open_delay - timedelta.seconds + timedelta.microseconds / 1000000
                if delay > 0:
                    logger.log(f'Placed Bet to Open delay: {delay:.2f} seconds')
                    sleep(delay)
            
            selection_button.click(container_css_selector='.ipe-EventViewDetailScroller', scrollable_section_css_selector='.ipe-EventViewDetail_ContentContainer')

            logger.log(f'self.settings.open_coupon_wait_time = {self.settings.open_coupon_wait_time}')
            self.browser.node('Betslip', betslip_selector, timeout=self.settings.open_coupon_wait_time, not_found_error='Betslip not opened', not_found_error_type=ErrorType.BETSLIP_DID_NOT_OPENED)
                    
            steps.check_bet_name(self)
            
            return

        except BotError as error:
            last_error = error
            if error.type == ErrorType.WRONG_BET_OPENED or error.type == ErrorType.BETSLIP_DID_NOT_OPENED:
                steps.clear_betslip(self)
            else:
                raise error
    
    raise last_error