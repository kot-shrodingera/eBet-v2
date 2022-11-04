import re

from ...browser import Browser
from ...errors import BotError, ErrorType
from ... import logger

referral_accepted_selector = '.bss-ReferralInfo_Label-accepted'
referral_declined_selector = '.bss-ReferralInfo_Label-partialdecline'
referral_result_selector = f'{referral_accepted_selector}, {referral_declined_selector}'

def get_traders_accepted_amount(browser: Browser) -> float:
    logger.log('Getting Traders Accepted Amount')
    
    referral_result = browser.node('Traders Result', referral_result_selector)
    
    referral_result_text = referral_result.get_property('textContent').replace(',', '')
    referral_result_value_regex = r'^(?:.*?)?(\d+\.\d+)'
    referral_result_value_match = re.search(referral_result_value_regex, referral_result_text)
    if not referral_result_value_match:
        raise BotError('Cannot parse traders amount')
    referral_result_amount = float(referral_result_value_match[1])
    logger.log(f'Referral Amount: {referral_result_amount}')
    
    referral_accepted = browser.node('Traders Acceptred', referral_accepted_selector, 0, required=False)
    if referral_accepted:
        logger.log('Traders Accepted')
        return referral_result_amount
    
    referral_declined = browser.node('Traders Declined', referral_declined_selector, 0, required=False)
    if referral_declined:
        logger.log('Traders Declined')
        return 0
    
    raise BotError('Cannot get traders result', ErrorType.CANNOT_GET_TRAIDERS_RESULT)
