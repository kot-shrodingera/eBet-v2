from ... import logger
from ...browser import Browser

my_bets_filter_button_selector = '.myb-HeaderButton'

def check_cashout_tab(browser: Browser) -> bool:
    browser.node('My Bets Filter Buttons', my_bets_filter_button_selector)
    script = '''
() => {
    const myBetsFilterButtons = [...document.querySelectorAll('.myb-HeaderButton')];
    if (myBetsFilterButtons.length === 0) {
        return 'My Bets Filter Buttons not found';
    }
    const cashOutFilterButton = myBetsFilterButtons.find(
        (button) =>
            button.textContent === 'Cash Out' ||
            button.textContent === 'Chiudi Scommessa', // Italian
        );
    if (!cashOutFilterButton || [...cashOutFilterButton.classList].includes('Hidden')) {
        return 'Cash Out Filter Button not found';
    }
    return 'Cash Out Filter Button found';
}
'''
    result = browser.run_js_function(script)
    if 'result' in result and 'result' in result['result'] and 'value' in result['result']['result']:
        if result['result']['result']['value'] == 'Cash Out Filter Button found':
            return True
        logger.log(result['result']['result']['value'])
    else:
        logger.log('Error checking Cash Out tab')
        logger.log(result)
    return False