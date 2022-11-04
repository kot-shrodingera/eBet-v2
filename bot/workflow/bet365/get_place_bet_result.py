import re

from ... import logger
from ...browser import Browser, cr_exceptions



placed_selector = '.bss-ReceiptContent_Title'
error_selector = '.bs-DefaultMessage_MessageText, .bs-OpportunityChangeErrorMessage, .bss-StandardBetslip_Error, .bs-BetslipReferralsMessage_Title'
error_without_traders_selector = '.bs-DefaultMessage_MessageText, .bs-OpportunityChangeErrorMessage, .bss-StandardBetslip_Error'
result_selector = f'{placed_selector}, {error_selector}'

def get_place_bet_result(browser: Browser) -> str:
    result_message = browser.node('Result', result_selector, 15000)
    if not result_message:
        return 'No Result'

    try:
        error = browser.node('Error', error_selector, 0, required=False)
        if error:
            logger.log('Error')
            error_text = error.get_property('textContent')
            logger.log(error_text)
            
            account_restricted_regex = r'Certain restrictions may be applied to your account. If you have an account balance you can request to withdraw these funds now by going to the Withdrawal page in Members.'
            selection_changed_regex = r'The line and price of your selection changed|The price and availability of your selection changed|The availability of your selection changed|The selection is no longer available|The price of your selection changed|The price of your selection has changed|The line, odds or availability of your selections has changed.|The line, odds or availability of selections on your betslip has changed. Please review your betslip|La linea, le quote o la disponibilità delle tue selezioni è cambiata.'
            check_my_bets_regex = r'Please check My Bets for confirmation that your bet has been successfully placed.'
            referrals_regex = r'Part of your bet needs to be approved by a trader'
            
            if re.search(account_restricted_regex, error_text):
                return 'Account Restricted'
            if re.search(selection_changed_regex, error_text):
                return 'Odds Changed'
            if re.search(check_my_bets_regex, error_text):
                return 'Check My Bets'
            if re.search(referrals_regex, error_text):
                return 'Traders'
        
        placed = browser.node('Placed', placed_selector, 0, required=False)
        if placed:
            return 'Bet Placed'
        else:
            logger.log('No Result or Error found (!)')
            
        return 'Unknown Result'
    except cr_exceptions.ChromeError as chromeError:
        if 'Cannot find context with specified id' in str(chromeError):
            logger.log('Context Destroyed. Probably logout')
            return 'Logout'
        raise chromeError


