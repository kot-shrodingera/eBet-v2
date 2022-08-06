import random

from timeout import random_timeout # pyright: reportMissingTypeStubs=false

from ... import logger
from ...browser import Browser

def close_popups(browser: Browser) -> None:
    # time_log('Closing popups')
    
    accept_cookies_selector = '.ccm-CookieConsentPopup_Accept'
    # TODO: remove log
    accept_cookies = browser.node('Accept Cookies', accept_cookies_selector, 1, required=False)
    if accept_cookies:
        accept_cookies.click()

    # .iip-IntroductoryPopup_Cross is for Live Match Stats alert
    # .ccm-CookieConsentPopup_Accept to accept cookies
    popup_selectors = '.iip-IntroductoryPopup_Cross, .ccm-CookieConsentPopup_Accept'
    if browser.crdi.check(popup_selectors): # pyright: ignore [reportUnknownMemberType]
        popups = browser.crdi.finds(popup_selectors) # pyright: ignore [reportUnknownVariableType, reportUnknownMemberType]
        for popup in popups: # pyright: ignore [reportUnknownVariableType, reportUnusedVariable]
            browser.crdi.click(popup_selectors) # pyright: ignore [reportUnknownMemberType]
            logger.log('Closed bet365 popup\n')
            random_timeout(0, 1)

    ## Close bet365 popups
    notification_frame = browser.crdi.check('.lp-UserNotificationsPopup_Frame') # pyright: ignore [reportUnknownVariableType, reportUnknownMemberType]
    if notification_frame:
        # #remindLater is when the credit card is about to expire
        # #ConfirmButton is for confirm contact details prompt
        # #KeepCurrentLimitsButton is for deposit limits prompt
        notification_selectors = '#yesButton, #ConfirmButton, #remindLater, #KeepCurrentLimitsButton'
        close_buttons = browser.crdi.finds(notification_selectors, iframe=True) # pyright: ignore [reportUnknownVariableType, reportUnknownMemberType]
        for top_coordinate, right_coordinate, bottom_coordinate, left_coordinate in close_buttons: # pyright: ignore [reportUnknownVariableType]
            x_coordinate = random.uniform(left_coordinate, right_coordinate) # pyright: ignore [reportUnknownArgumentType]
            y_coordinate = random.uniform(bottom_coordinate, top_coordinate) # pyright: ignore [reportUnknownArgumentType]
            browser.crdi.click_item_at_coords(x_coordinate, y_coordinate) # pyright: ignore [reportUnknownMemberType]
            logger.log('Closed bet365 notification popup')
            random_timeout(0, 1)

    # .pm-MessageOverlayCloseButton is for new messages
    # .llm-LastLoginModule_Button is the last login time (only shows up for certain countries)
    # .pm-PushTargetedMessageOverlay_CloseButton is for new messages
    popup_selectors = '.pm-MessageOverlayCloseButton, .alm-ActivityLimitStayButton, .pm-FreeBetsPushGraphicCloseIcon, .llm-LastLoginModule_Button, .pm-PushTargetedMessageOverlay_CloseButton, .pm-MessageOverlayCloseButton'
    if browser.crdi.check(popup_selectors): # pyright: ignore [reportUnknownMemberType]
        popups = browser.crdi.finds(popup_selectors) # pyright: ignore [reportUnknownVariableType, reportUnknownMemberType]
        for popup in popups: # pyright: ignore [reportUnknownVariableType, reportUnusedVariable]
            browser.crdi.click(popup_selectors) # pyright: ignore [reportUnknownMemberType]
            logger.log('Closed bet365 popup')
            random_timeout(0, 1)

    # logger.log('Popups closed')
