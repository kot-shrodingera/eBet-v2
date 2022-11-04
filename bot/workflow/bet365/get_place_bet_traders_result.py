from ...browser import Browser



placed_selector = '.bss-ReceiptContent_Title'

def get_place_bet_traders_result(browser: Browser) -> bool:
    placed = browser.node('Placed (After Traders)', placed_selector, 60000)
    if not placed:
        return False
    return True
