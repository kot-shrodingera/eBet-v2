from typing import Optional

from ...browser import Browser



def get_selection_button(browser: Browser, market: str, column: Optional[str], selection: str):
    function = '''
(market, column, selection) => {
    const marketTitles = [
        ...document.querySelectorAll(
            '.sip-MarketGroupButton',
        ),
    ];
    const marketTitle = marketTitles.find((marketTitles) => {
        return marketTitles.textContent.trim() === market;
    });
    if (!marketTitle) {
        return "Market Title not found";
    }
    // const marketElement = marketTitle.closest('.sip-MarketGroup')
    const marketElement = marketTitle.parentElement;
    if (!marketElement) {
        return "Market Group not found";
    }
    let betButton;
    if (column === 'Over') {
        betButton = marketElement.querySelector('.gl-Market:nth-of-type(2) > .gl-Participant_General');
    } else if (column === 'Under') {
        betButton = marketElement.querySelector('.gl-Market:nth-of-type(3) > .gl-Participant_General');
    // } else if (market === '3-Way Handicap') {
    } else if (marketElement.querySelector('.gl-MarketColumnHeader')) {
		// betButton = document.evaluate(`.//*[text()="${selection}"]`, marketElement).iterateNext().nextElementSibling;
        const xpath = `.//div[contains(concat(' ', @class, ' '), ' gl-MarketColumnHeader ')][text()="${selection}"]`
        const betHeader = document.evaluate(xpath, marketElement).iterateNext();
        if (betHeader) {
            betButton = betHeader.nextElementSibling;
        }
	} else { // Standard markets
        // betButton = document.evaluate(`.//*[text()="${selection}"]`, marketElement).iterateNext();
        const xpath = `.//div[contains(concat(' ', @class, ' '), ' gl-Participant_General ')]/span[text()="${selection}"]/..`
        betButton = document.evaluate(xpath, marketElement).iterateNext();
    }
    if (!betButton) {
        return "Selection Button not found"
    }
    return betButton;
}
'''
    return browser.process_js_return(browser.run_js_function(function, [market, column, selection]), 'Selection Button')
