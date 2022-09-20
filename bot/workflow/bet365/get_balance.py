import re

from typing import TypedDict

from ...browser import Browser
from ...errors import BotError


balance_selector = '.hm-Balance'

class Balance(TypedDict):
    balance: float
    currency: str

def get_balance(browser: Browser) -> Balance:
    balance = browser.node('Balance', balance_selector, empty_text_allowed=False)
    balance_text = balance.get_property('textContent').replace(',', '')
    balance_regex_1 = r'^(.*?)(\d+\.\d+)$'
    balance_match_1 = re.search(balance_regex_1, balance_text)
    if balance_match_1:
        if balance_match_1[1] == '$':
            currency = 'USD'
        elif balance_match_1[1] == '£':
            currency = 'GBP'
        elif balance_match_1[1] == '€':
            currency = 'EUR'
        elif balance_match_1[1] == 'RS. ':
            currency = 'INR'
        else:
            raise BotError(f'Cannot parse currency: {balance_text}')
        return { 'balance': float(balance_match_1[2]), 'currency': currency}
    balance_regex_2 = r'^(\d+\.\d+)\s+(.+)$'
    balance_match_2 = re.search(balance_regex_2, balance_text)
    if balance_match_2:
        if balance_match_2[2] == 'CHF':
            currency = 'CHF'
        else:
            raise BotError(f'Cannot parse currency: {balance_text}')
        return { 'balance': float(balance_match_2[1]), 'currency': currency}
    raise BotError(f'Cannot parse balance: {balance_text}')
