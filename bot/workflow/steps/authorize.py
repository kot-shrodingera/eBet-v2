from time import sleep

from .. import Workflow, bet365

from ... import logger
from ...errors import BotError


member_icon_selector = '.hm-MainHeaderMembersWide_MembersMenuIcon, .hm-MainHeaderMembersNarrow_MembersMenuIcon'
auth_form_button_selector = '.hm-MainHeaderRHSLoggedOutWide_Login, .hm-MainHeaderRHSLoggedOutMed_Login, .hm-MainHeaderRHSLoggedOutNarrow_Login'
username_input_selector = '.lms-StandardLogin_Username'
clear_username_input_selector = '.lms-StandardLogin_UsernameControl'
password_input_selector = '.lms-StandardLogin_Password'
login_button_selector = '.lms-LoginButton'

def authorize(self: Workflow) -> None:
    self.browser.go_to_url(self.bet365_my_bets_url)
    
    self.browser.create_isolated_world()
    sleep(0.25)
    
    bet365.close_popups(self.browser)
    
    member_icon = self.browser.node('Member Icon', member_icon_selector, timeout=2000, required=False)
    if member_icon:
        logger.log(f'Already authorized (Balance: {bet365.get_balance(self.browser)})')
    else:
        logger.log(f'Not authorized. Authorizing as {self.settings.username}')

        auth_form_button = self.browser.node('Auth Form Button', auth_form_button_selector)
        auth_form_button.click()

        sleep(1) # some delay is required for clearing to work

        username_input = self.browser.node('Username Input', username_input_selector)

        username_value = username_input.get_property('value')
        if username_value != self.settings.username:
            if username_value != '':
                logger.log('Clearing username')
                clear_username_input = self.browser.node('Clear Username Input', clear_username_input_selector)
                clear_username_input.click()
            else:
                username_input.click()
            logger.log('Typing username')
            self.browser.crdi.send(self.settings.username)
        
        password_input = self.browser.node('Password input', password_input_selector)
        logger.log('Typing password')
        password_input.click()
        self.browser.crdi.send(self.settings.password)

        login_button = self.browser.node('Login Button', login_button_selector)
        login_button.click()

        logger.log('Waiting 5 seconds for page to reload')
        sleep(5)

        self.browser.create_isolated_world()

        member_icon = self.browser.node('Member Icon', member_icon_selector)
        logger.log(f'Auth Successful (Balance: {bet365.get_balance(self.browser)})')
    
    bet365.close_popups(self.browser)

    self.browser.go_to_url(self.bet365_my_bets_url)
    
    if not bet365.check_cashout_tab(self.browser):
        self.porez = True
        if self.settings.dont_pause_on_porez:
            return
        raise BotError('Pause on Porez')
