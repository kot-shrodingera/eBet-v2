from ...browser import Browser
from ...errors import BotError

selection_name_selector = '.bss-NormalBetItem_Title'

def get_selection_name(browser: Browser) -> str:
    selection_name = browser.node('Selection Name', selection_name_selector, 0)
    
    return selection_name.get_property('textContent')
