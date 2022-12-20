import random

from timeout import random_timeout

from ... import logger
from ...browser import Browser

def close_popups(browser: Browser) -> None:
    # time_log('Closing popups')

    # .iip-IntroductoryPopup_Cross is for Live Match Stats alert
    # .ccm-CookieConsentPopup_Accept to accept cookies
    popup_selectors = '.iip-IntroductoryPopup_Cross, .ccm-CookieConsentPopup_Accept'
    if browser.crdi.check(popup_selectors):
        popups = browser.crdi.finds(popup_selectors)
        for popup in popups:
            browser.crdi.click(popup_selectors)
            logger.log('Closed bet365 popup')
            random_timeout(0, 1)
    
    ## Close bet365 popups
    notification_frame = browser.crdi.check('.lp-UserNotificationsPopup_Frame')
    if notification_frame:
        # #remindLater is when the credit card is about to expire
        # #ConfirmButton is for confirm contact details prompt
        # #KeepCurrentLimitsButton is for deposit limits prompt
        # .wmeCloseButton is for Only gamble what you can afford to lose
        notification_selectors = '#yesButton, #ConfirmButton, #remindLater, #KeepCurrentLimitsButton, .wmeCloseButton'
        close_buttons = browser.crdi.finds(notification_selectors, iframe=True)
        for close_button in close_buttons:
            browser.crdi.click_coords(close_button['coordinates'])
            logger.log('Closed bet365 notification popup')
            random_timeout(1)

    # .pm-MessageOverlayCloseButton is for new messages
    # .llm-LastLoginModule_Button is the last login time (only shows up for certain countries)
    # .pm-PushTargetedMessageOverlay_CloseButton is for new messages
    popup_selectors = '.pm-MessageOverlayCloseButton, .alm-ActivityLimitStayButton, .alm-InactivityAlertRemainButton, .pm-FreeBetsPushGraphicCloseIcon, .llm-LastLoginModule_Button, .pm-PushTargetedMessageOverlay_CloseButton'
    if browser.crdi.check(popup_selectors):
        popups = browser.crdi.finds(popup_selectors)
        for popup in popups:
            browser.crdi.click(popup_selectors)
            logger.log('Closed bet365 popup')
            random_timeout(1)

    # logger.log('Popups closed')
