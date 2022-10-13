from ...browser import Browser
from ...errors import BotError

market_name_selector = '.bss-NormalBetItem_Market'

def get_market_name(browser: Browser) -> str:
    market_name = browser.node('Market Name', market_name_selector, 0)
    
    return market_name.get_property('textContent')
