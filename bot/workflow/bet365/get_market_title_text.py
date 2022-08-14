from ...browser import Browser


def get_market_title_text(browser: Browser, market: str):
    function = '''
(market) => {
    const marketTitleTexts = [
        ...document.querySelectorAll(
            '.sip-MarketGroupButton_Text',
        ),
    ];
    const marketTitleText = marketTitleTexts.find((marketTitleText) => {
        return marketTitleText.textContent.trim() === market;
    });
    if (!marketTitleText) {
        return 'Market Title Text not found'
    }
    return marketTitleText;
}
'''
    return browser.process_js_return(browser.run_js_function(function, [market]), 'Market Title')
