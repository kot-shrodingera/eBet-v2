import re

from ... import logger
from ...browser import Browser



placed_selector = '.bss-ReceiptContent_Title'
error_selector = '.lqb-QuickBetHeader_HasMessage .lqb-QuickBetHeader_MessageBody, .bs-OpportunityChangeErrorMessage'
result_selector = f'{placed_selector}, {error_selector}'

bet_placed_class = 'bss-ReceiptContent_Title'
odds_changed_class = 'bs-OpportunityChangeErrorMessage'
deposit_required_class = 'qd-QuickDepositModule'

def get_place_bet_result(browser: Browser) -> str:
    result_message = browser.node('Result', result_selector, 15000)
    if not result_message:
        return 'No Result'
    
    placed = browser.node('Placed', placed_selector, 0, required=False)
    if placed:
        return 'Bet Placed'
    
    error = browser.node('Error', error_selector, 0, required=False)
    if error:
        error_text = error.get_property('textContent')
        logger.log(error_text)
        
        selection_changed_regex = r'The line and price of your selection changed|The price and availability of your selection changed|The availability of your selection changed|The selection is no longer available|The price of your selection changed|The price of your selection has changed|The line, odds or availability of your selections has changed.|The line, odds or availability of selections on your betslip has changed. Please review your betslip|La linea, le quote o la disponibilità delle tue selezioni è cambiata.'
        check_my_bets_regex = r'Please check My Bets for confirmation that your bet has been successfully placed.'
        
        if re.search(selection_changed_regex, error_text):
            return 'Odds Changed'
        if re.search(check_my_bets_regex, error_text):
            return 'Check My Bets'
        
        
    else:
        logger.log('No Result or Error found (!)')
        
    return 'Unknown Result'
