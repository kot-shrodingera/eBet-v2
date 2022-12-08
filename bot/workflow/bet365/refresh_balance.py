# from ... import logger
from ...browser import Browser

# member_icon_selector = '.hm-MainHeaderMembersWide_MembersMenuIcon'
# balance_refresh_icon_selector = '.um-BalanceRefreshButton_Icon'

def refresh_balance(browser: Browser) -> None:
    # member_icon = browser.node('Member Icon', member_icon_selector, 1, required=False)
    # if not member_icon:
    #     logger.log('No Member Icon. Cannot refresh balance')
    #     return
    
    # member_icon.click()
    
    # balance_refresh_icon = browser.node('Balance Refresh Icon', balance_refresh_icon_selector, 1, required=False)
    # if not balance_refresh_icon:
    #     logger.log('No Balance Refresh Icon. Cannot refresh balance')
    #     return

    # balance_refresh_icon.click()
    # logger.log('Balance Refreshed')
    
    # member_icon.click()
    
    browser.run_js_function('''
() => {
    Locator.user._balance.refreshBalance();
}
''')
