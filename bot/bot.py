import os
import urllib.parse
import requests

from datetime import datetime

from ChromeController import ChromeContext

from . import logger
from .settings import Settings
from .browser import Browser
from .workflow import Workflow
from .control import Control


class Bot:
    settings: Settings
    browser: Browser
    control: Control
    bot_version = '2.0.44'
    
    ebet_auth_token: str
    first_launch: bool
    
    start_time = datetime.now()
    placed_bets_count: int = 0
    bets_tries_count: int = 0
    
    def __init__(self, settings__file_name: str) -> None:
        self.settings = Settings(settings__file_name)
        self.control = Control()
        self.first_launch = not os.path.exists(f'./profiles/{self.settings.username}')
        
        query_data = {
            'api[method]': 'auth',
            'api[version]': '1',
            'api_key': self.settings.api_key,
            'password': self.settings.api_password,
            'bot_version': self.bot_version,
        }
        query_string = urllib.parse.urlencode(query_data)
        response = requests.get(f'http://bvb.strike.ws/bot/index.php?{query_string}').json()
        if 'data' not in response or 'token' not in response['data']:
            raise Exception('No token in eBet auth response')
        self.ebet_auth_token = response['data']['token']

    def run(self) -> None:
        additional_options = [
            # '--start-maximized'
        ]
        if self.settings.window_width and self.settings.window_height:
            additional_options.append(f'--window-size={self.settings.window_width},{self.settings.window_height}')
             
            
        while True:
            

            with ChromeContext(binary=f'"{self.settings.chrome_binary_path}"',
                               profile_username=self.settings.username,
                               start_maximised=False,
                               additional_options=additional_options,
                               port=self.settings.chrome_port) as crdi:
                self.browser = Browser(crdi,
                                       self.settings)
                
                if self.first_launch:
                    self.first_launch = False
                    logger.header('First Launch')
                    
                    self.browser.crdi.get('https://chrome.google.com/webstore/detail/webrtc-leak-prevent/eiadekoaikejlgdbkbdfeijglgfdalml')
                    logger.log('1) Install WebRTC Leak Prevent extension')
                    logger.log('2) Set last option (IP handling policy: Disable non-proxied UDP (force proxy))')
                    logger.log('3) Close extension settings modal')
                    logger.log('4) Close extension settings chrome tab')
                    logger.log('Press Enter to continue, or type q to quit')
                    choice = input()
                    if choice.lower() == 'q':
                        return
                    
                    self.browser.crdi.get('https://chrome.google.com/webstore/detail/disable-html5-autoplay-re/cafckninonjkogajnihihlnnimmkndgf')
                    logger.log('1) Install Disable HTML5 Autoplay extension')
                    logger.log('Press Enter to continue, or type q to quit')
                    choice = input()
                    if choice.lower() == 'q':
                        return
                    
                    self.browser.crdi.get('https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif/related')
                    logger.log('1) Install Proxy SwitchyOmega extension [if needed]')
                    logger.log('1) Setup proxy [if needed]')
                    logger.log('Press Enter to continue, or type q to quit')
                    choice = input()
                    if choice.lower() == 'q':
                        return
                if self.settings.dev:
                    logger.log('Dev Run')
                    Workflow(self.settings, self.ebet_auth_token, self.browser, self.control, self.bot_version, self.start_time, self.placed_bets_count, self.bets_tries_count).dev()
                    logger.log('Stop bot')
                    while self.control.get_current_action() != 'stop':
                        pass
                    break
                else:
                    result = Workflow(self.settings, self.ebet_auth_token, self.browser, self.control, self.bot_version, self.start_time, self.placed_bets_count, self.bets_tries_count).run()
                    if type(result) is bool:
                        if result is False:
                            if self.control.current_action == 'stop':
                                break
                            logger.log('Press Enter to close Bot')
                            input()
                            break
                        # else:
                    else:
                        (placed_bets_count, bets_tries_count) = result
                        self.placed_bets_count += placed_bets_count
                        self.bets_tries_count += bets_tries_count
                        logger.log('Restarting browser')
                        self.control.set_current_action('init')
                
             
        self.control.set_current_action('stopped')   
        # logger.log('Press Enter to close Bot')
        # input()
