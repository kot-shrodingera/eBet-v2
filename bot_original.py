import os, random, requests
from configparser import ConfigParser
from ChromeController import ChromeRemoteDebugInterface
from timeout import random_timeout
from printr import printr, current_time

# pip install requests ChromeController python_ghost_cursor python-timeout python-printr
# WebRTC block extension: https://chrome.google.com/webstore/detail/webrtc-leak-prevent/eiadekoaikejlgdbkbdfeijglgfdalml

# VPS: 185.230.143.63 / 6vb9rin4jidp84D1

settings = ConfigParser()
settings.read('settings.ini')
username = settings['Settings']['username']
password = settings['Settings']['password']
stake = settings['Settings']['stake']
bet365_url = settings['Settings']['bet365_url']
api_key = settings['Settings']['api_key']
api_password = settings['Settings']['api_password']

response = requests.get(f'http://bvb.strike.ws/bot/index.php?api[method]=auth&api[version]=1&api_key={api_key}&password={api_password}').json()
# printr('Response:', response)

auth = {'data[token]': (None, response['data']['token'])}

# while True:
#     response = requests.post('http://bvb.strike.ws/bot/index.php?api[method]=get_forks&api[version]=1', files=auth).json()
#     # printr('Response:', response)
#     for bet_details in response['data']['forks']:
#         printr(bet_details)
#         match_link = bet_details['bet365_direct_link']
#         updated_match_link = match_link.replace('https://www.bet365.com', bet365_url)
#         market = bet_details['bet365_market']
#         selection = bet_details['bet365_selection']
#         minimum_odds = float(bet_details['coef'])
#         print('Received new bet')
#         print('Match link:', match_link)
#         print('Market:', market)
#         print('Selection:', selection)
#         input('Next?')
#     random_timeout(1, 2)

additional_options = [f'--user-data-dir={os.getcwd()}/profiles/{username}', '--start-maximized']
binary_path = '"C:/Program Files/Google/Chrome/Application/chrome.exe"'
browser = ChromeRemoteDebugInterface(binary=binary_path, additional_options=additional_options)
# input()

browser.get(bet365_url + '#/IP/B1')
random_timeout(1, 2)
page_loaded = browser.wait_for('.ovm-ClassificationHeader_Text')
if not page_loaded: # Check bet365 doesn't need reloading
    print('Reloading bet365')
    print()
    browser.reload()
    random_timeout(1, 2)
    browser.create_isolated_world()
    browser.wait_for('.ovm-ClassificationHeader_Text')

# .iip-IntroductoryPopup_Cross is for Live Match Stats alert
# .ccm-CookieConsentPopup_Accept to accept cookies
popup_selectors = '.iip-IntroductoryPopup_Cross, .ccm-CookieConsentPopup_Accept'
if browser.check(popup_selectors):
    popups = browser.finds(popup_selectors)
    for popup in popups:
        browser.click(popup_selectors)
        print('Closed bet365 popup')
        print()
        random_timeout(0, 1)

def setup_bet365():
    # Login
    if browser.check('.hm-MainHeaderRHSLoggedOutWide_Login, .hm-MainHeaderRHSLoggedOutMed_Login, .hm-MainHeaderRHSLoggedOutNarrow_Login'):
        print('Logging in as', username)
        browser.click('.hm-MainHeaderRHSLoggedOutWide_Login, .hm-MainHeaderRHSLoggedOutMed_Login, .hm-MainHeaderRHSLoggedOutNarrow_Login')
        random_timeout(0, 1)
        if browser.wait_for('.lms-StandardLogin_Username'):
            username_value = browser.get_value('.lms-StandardLogin_Username')
            if username_value != username: # Check value of username input, if username is already there then it will type in password input
                browser.send(username)
                random_timeout(0, 1)
                browser.click('.lms-StandardLogin_Password')
                random_timeout(0, 1)
            browser.send(password)
            random_timeout(0, 1)
            browser.click('.lms-LoginButton')
            random_timeout(3, 4)
            browser.create_isolated_world()
            if browser.wait_for('.hm-MainHeaderMembersWide_MembersMenuIcon, .hm-MainHeaderMembersNarrow_MembersMenuIcon'):
                print('Logged in as', username)
            else:
                print('Error when trying to login as', username, 'is the password correct?')
        else:
            print('Error when trying to login as', username)

    ## Close bet365 popups
    notification_frame = browser.check('.lp-UserNotificationsPopup_Frame')
    if notification_frame:
        # #remindLater is when the credit card is about to expire
        # #ConfirmButton is for confirm contact details prompt
        # #KeepCurrentLimitsButton is for deposit limits prompt
        notification_selectors = '#yesButton, #ConfirmButton, #remindLater, #KeepCurrentLimitsButton'
        close_buttons = browser.finds(notification_selectors, iframe=True)
        for top_coordinate, right_coordinate, bottom_coordinate, left_coordinate in close_buttons:
            x_coordinate = random.uniform(left_coordinate, right_coordinate)
            y_coordinate = random.uniform(bottom_coordinate, top_coordinate)
            browser.click_item_at_coords(x_coordinate, y_coordinate)
            print('Closed bet365 notification popup')
            print()
            random_timeout(0, 1)

    # .pm-MessageOverlayCloseButton is for new messages
    # .llm-LastLoginModule_Button is the last login time (only shows up for certain countries)
    # .pm-PushTargetedMessageOverlay_CloseButton is for new messages
    popup_selectors = '.pm-MessageOverlayCloseButton, .alm-ActivityLimitStayButton, .pm-FreeBetsPushGraphicCloseIcon, .llm-LastLoginModule_Button, .pm-PushTargetedMessageOverlay_CloseButton, .pm-MessageOverlayCloseButton'
    if browser.check(popup_selectors):
        popups = browser.finds(popup_selectors)
        for popup in popups:
            browser.click(popup_selectors)
            print('Closed bet365 popup')
            print()
            random_timeout(0, 1)
    
    if browser.check('.bss-RemoveButton, .bss-ReceiptContent_Done'):
        print('Closing old betslip')
        print()
        browser.click('.bss-RemoveButton, .bss-ReceiptContent_Done')
        random_timeout(0, 1)

setup_bet365()

browser.get('chrome://newtab') # Navigate away from bet365 to prevent error when navigating to match page

# Get old bets
response = requests.post('http://bvb.strike.ws/bot/index.php?api[method]=get_forks&api[version]=1', files=auth).json()
# printr('Response:', response)
placed_bets = response['data']['forks']

while True:
    response = requests.post('http://bvb.strike.ws/bot/index.php?api[method]=get_forks&api[version]=1', files=auth).json()
    for bet_details in response['data']['forks']:
        # printr(bet_details)
        if bet_details not in placed_bets:
            match_link = bet_details['bet365_direct_link']
            updated_match_link = match_link.replace('https://www.bet365.com', bet365_url)
            bet_selection = bet_details['bet365_bet_name']
            print('bet_selection:', bet_selection)
            selection_details = bet_selection.split('|')
            column = None
            if len(selection_details) == 2:
                market, selection = selection_details
            elif len(selection_details) == 3:
                market, selection, column = selection_details
            elif len(selection_details) == 4:
                market, alternative_selection_name, selection, column = selection_details

            minimum_odds = 1.1 # float(bet_details['max_lower_coef_percent'])
            print('Received new bet')
            print('Match link:', match_link)
            print('Market:', market)
            print('Selection:', selection)
            print('Minimum odds:', minimum_odds)

            browser.get(match_link)
            browser.create_isolated_world()
            browser.wait_for('.ipe-EventHeader_Fixture, .ml1-LocationEventsMenu_Text, .sph-EventHeader') # Wait for match page to load

            setup_bet365()
        
            browser.scroll_to(container_css_selector='.ipe-EventViewDetailScroller', amount=1) # Scroll once to load all markets
            random_timeout(1)

            setup_bet365()

            place_bet_result = False
            
            result = browser.execute_javascript_function(f'''
                function get_bet_button() {{
                    let market_title_element = document.evaluate('//*[starts-with(text(), "{market}")]', document).iterateNext()
                    if (!market_title_element) return "Couldn't find market title"
                    let market = market_title_element.closest('.sip-MarketGroup') // Traverse up to market element
                    if (!market) return "Couldn't find market element"
                    if ('{column}' == 'Over') {{
                        var bet_button = market.querySelector('.gl-Market:nth-of-type(2) > .gl-Participant_General')
                        }}
                    else if ('{column}' == 'Under') {{
                        var bet_button = market.querySelector('.gl-Market:nth-of-type(3) > .gl-Participant_General')
                        }}
                    else {{ // Standard markets
                        var bet_button = document.evaluate('.//*[text()="{selection}"]', market).iterateNext()
                        }}
                    if (!bet_button) return "Couldn't find bet selection button"
                    let suspended_check = bet_button.classList.value.includes('Suspended') // Suspended check uses different class names based on the bet button class
                    if (suspended_check) return "Betting suspended"
                    let bet_button_coordinates = bet_button.getBoundingClientRect()
                    return [bet_button_coordinates.top, bet_button_coordinates.right, bet_button_coordinates.bottom, bet_button_coordinates.left]
                    }}''')
            print('get_bet_button() result:', result)

            if type(result['value']) == list: # Error return will be a string
                print('Clicking selection')
                print()
                bet_button_top_coordinate, bet_button_right_coordinate, bet_button_bottom_coordinate, bet_button_left_coordinate = result['value']
                bet_button_x_coordinate = random.uniform(bet_button_left_coordinate, bet_button_right_coordinate)
                bet_button_y_coordinate = random.uniform(bet_button_bottom_coordinate, bet_button_top_coordinate)
                scroll_amount = browser.scroll_to(bet_button_y_coordinate)
                current_y_coordinate = bet_button_y_coordinate - scroll_amount
                browser.click_item_at_coords(bet_button_x_coordinate, current_y_coordinate) # Click bet selection and open betslip
                random_timeout(1, 2)
                browser.create_isolated_world()

                if browser.wait_for('.bs-AnimationHelper_ContainerNoScale'): # If betslip open
                    # Check stake and change if needed
                    current_stake = browser.get_text('.bsf-StakeBox_StakeValue-input')
                    if current_stake != stake:
                        browser.click('.bsf-StakeBox_StakeUnits, .bsf-StakeBox_StakeValue-input.bsf-StakeBox_StakeValue-empty') # If stake is set already, click on the units selector to highlight stake input and overwrite it
                        random_timeout(0, 1)
                        browser.send(stake)
                        random_timeout(0, 1)
                        if not browser.check('.bsf-RememberStakeButtonNonTouch-active'): # Remember stake button already toggled
                            browser.click('.bsf-RememberStakeButtonNonTouch_HitArea')
                            random_timeout(0, 1)
                    
                    # Check odds
                    current_odds = float(browser.get_text('.bsc-OddsDropdownLabel > span'))
                    if current_odds >= minimum_odds:
                        browser.click('.bsf-PlaceBetButton:not(.Hidden), .bsf-AcceptButton:not(.Hidden)') # Place bet button
                        random_timeout(1, 2)
                        browser.create_isolated_world()
                        if browser.wait_for('.bss-ReceiptContent_Title, .bs-OpportunityChangeErrorMessage, .qd-QuickDepositModule'): # 'Bet Placed' text, odds changed message or deposit required message
                            if browser.check('.bss-ReceiptContent_Title'): # 'Bet Placed' text
                                place_bet_message = browser.get_text('.bss-ReceiptContent_Title')
                                place_bet_result = True
                                browser.click('.bss-ReceiptContent_Done')
                                random_timeout(0, 1)
                            elif browser.check('.bs-OpportunityChangeErrorMessage'): # Recheck odds and retry bet placement if odds are within allowed range
                                print('Odds changed, retrying')
                                def retry_bet():
                                    for retry_attempt in range(10):
                                        current_odds = float(browser.get_text('.bsc-OddsDropdownLabel > span'))
                                        if current_odds >= minimum_odds:
                                            browser.click('.bsf-PlaceBetButton:not(.Hidden), .bsf-AcceptButton:not(.Hidden)') # Accept changed odds and place bet button
                                            random_timeout(1, 2)
                                            if browser.wait_for('.bss-ReceiptContent_Title, .bs-OpportunityChangeErrorMessage, .qd-QuickDepositModule'):
                                                if browser.check('.bss-ReceiptContent_Title'): # 'Bet Placed' text
                                                    place_bet_message = browser.get_text('.bss-ReceiptContent_Title')
                                                    place_bet_result = True
                                                    browser.click('.bss-ReceiptContent_Done')
                                                    random_timeout(1, 2)
                                                    return True, place_bet_message
                                                elif browser.check('.bs-OpportunityChangeErrorMessage'):
                                                    continue
                                                else:
                                                    return False, "Didn't bet: unknown error"
                                            else:
                                                return False, "Didn't bet: unknown error"
                                        else:
                                            return False, "Didn't bet - odds not above minimum"
                                    return False, "Didn't bet: odds changed more than ten times"
                                place_bet_result, place_bet_message = retry_bet()
                            elif browser.check('.qd-QuickDepositModule'):
                                place_bet_message = "Didn't bet - deposit required"
                            else:
                                place_bet_message = "Didn't bet - unknown error"
                        else:
                            place_bet_message = "Didn't bet - unknown error"
                    else:
                        place_bet_message = "Didn't bet - odds not above minimum"
                else:
                    place_bet_message = "Didn't bet - error when opening betslip"
            else:
                place_bet_message = result['value']
            
            current_time('Place bet result:')
            print(place_bet_message)
            print()

            ## Send place bet result to API
        
            if browser.check('.bss-RemoveButton, .bss-ReceiptContent_Done'):
                print('Closing betslip')
                print()
                browser.click('.bss-RemoveButton, .bss-ReceiptContent_Done')
                random_timeout(0, 1)
            
            browser.get('chrome://newtab') # Navigate away from bet365 to prevent error when navigating to match page

            placed_bets.append(bet_details)
    
    random_timeout(1, 2)