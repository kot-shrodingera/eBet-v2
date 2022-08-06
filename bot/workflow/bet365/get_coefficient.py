from ...browser import Browser
from ...errors import BotError


coefficient_selector = '.bsc-OddsDropdownLabel > span'

def get_coefficient(browser: Browser):
    coefficient = browser.node('Coefficient', coefficient_selector)
    coefficient_text = coefficient.get_property('textContent')
    if coefficient_text == 'SP':
        raise BotError('Selection is Suspended')
    coefficient_value = float(coefficient_text)
    return coefficient_value
