from typing import Union

from ...browser import Browser



def get_selection_button(browser: Browser, market: str, column: Union[str, None], selection: str) -> Union[str, None]:
    function = '''
(market, column, selection) => {
    const marketTitleElement = document.evaluate(`//*[starts-with(text(), "${market}")]`, document).iterateNext();
    if (!marketTitleElement) {
        return "Couldn't find market title";
    }
    const marketElement = marketTitleElement.closest('.sip-MarketGroup') // Traverse up to market element
    if (!marketElement) {
        return "Couldn't find market element";
    }
    let betButton;
    if (column === 'Over') {
        betButton = marketElement.querySelector('.gl-Market:nth-of-type(2) > .gl-Participant_General');
    } else if (column === 'Under') {
        betButton = marketElement.querySelector('.gl-Market:nth-of-type(3) > .gl-Participant_General');
    } else if (market === '3-Way Handicap') {
		betButton = document.evaluate(`.//*[text()="${selection}"]`, marketElement).iterateNext().nextElementSibling;
	} else { // Standard markets
        betButton = document.evaluate(`.//*[text()="${selection}"]`, marketElement).iterateNext();
    }
    if (!betButton) {
        return "Couldn't find bet selection button";
    }
    const suspendedCheck = betButton.classList.value.includes('Suspended'); // Suspended check uses different class names based on the bet button class
    if (suspendedCheck) {
        return "Betting suspended";
    }
    return betButton;
    // const betButtonCoordinates = betButton.getBoundingClientRect();
    // return [betButtonCoordinates.top, betButtonCoordinates.right, betButtonCoordinates.bottom, betButtonCoordinates.left];
}
'''
    result = browser.run_js_function(function, [market, column, selection])
    try:
        return result['result']['result']['objectId']
    except:
        return None
