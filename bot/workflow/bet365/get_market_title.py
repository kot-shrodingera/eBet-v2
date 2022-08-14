from ...browser import Browser


def get_market_title(browser: Browser, market: str):
    function = '''
(market) => {
    const marketTitles = [
        ...document.querySelectorAll(
            '.sip-MarketGroupButton',
        ),
    ];
    const titles = [];
    const marketTitle = marketTitles.find((marketTitles) => {
        const title = marketTitles.textContent.trim();
        titles.push(title);
        return title === market;
    });
    if (!marketTitle) {
        return `Market Title not found:\\n${titles.join('\\n')}`
    }
    return marketTitle;
}
'''
    return browser.process_js_return(browser.run_js_function(function, [market]), 'Market Title')
