from ...browser import Browser
from ...errors import BotError

bet_name_selector = '.bss-NormalBetItem_Title'

def get_bet_name(browser: Browser) -> str:
    bet_name = browser.node('Bet Name', bet_name_selector, 0)
    
    return bet_name.get_property('textContent')
