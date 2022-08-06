from ... import logger
from ...browser import Browser

my_bets_count_selector = '.hm-HeaderMenuItemMyBets_MyBetsCount'

def get_unsettled_bets_count(browser: Browser) -> int:
    my_bets_count = browser.node('My Bets Count', my_bets_count_selector, 1, required=False)
    if not my_bets_count:
        logger.log('No bets in play')
        return 0
    my_bets_count_text = my_bets_count.get_property('textContent')
    try:
        result = int(my_bets_count.get_property('textContent'))
        logger.log(f'My Bets Count: {result}')
        return result
    except ValueError:
        logger.log(f'Cannot parse My Bets Count ({my_bets_count_text})')
        return -1
