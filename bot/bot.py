import os
import requests

from datetime import datetime

from . import logger
from .settings import Settings
from .browser import Browser
from .browser.ChromeController import ChromeContext # pyright: reportUnknownVariableType=false
from .workflow import Workflow
from .control import Control


class Bot:
    settings: Settings
    browser: Browser
    control: Control
    bot_version = 'v2.0.2'
    
    ebet_auth_token: str
    first_launch: bool
    using_proxy: bool
    
    start_time = datetime.now()
    placed_bets_count: int = 0
    bets_tries_count: int = 0
    
    def __init__(self, settings__file_name: str) -> None:
        self.settings = Settings(settings__file_name)
        self.control = Control()
        self.first_launch = not os.path.exists(f'./profiles/{self.settings.username}')
        response = requests.get(f'http://bvb.strike.ws/bot/index.php?api[method]=auth&api[version]=1&api_key={self.settings.api_key}&password={self.settings.api_password}').json()
        if 'data' not in response or 'token' not in response['data']:
            raise Exception('No token in eBet auth response')
        self.ebet_auth_token = response['data']['token']

    def run(self) -> None:
        additional_options = [
            f'--user-data-dir={os.getcwd()}/profiles/{self.settings.username}',
            # '--start-maximized'
        ]
        if self.settings.window_width and self.settings.window_height:
            additional_options.append(f'--window-size={self.settings.window_width},{self.settings.window_height}')
             
        self.using_proxy = self.settings.proxy_enable != 0 and self.settings.proxy_ip != None and self.settings.proxy_port != None and self.settings.proxy_login != None and self.settings.proxy_pass != None
        if self.using_proxy:
            additional_options.append(f'--proxy-server={self.settings.proxy_ip}:{self.settings.proxy_port}')
            
        while True:
            

            with ChromeContext(binary=f'"{self.settings.chrome_binary_path}"', additional_options=additional_options) as crdi:
                self.browser = Browser(crdi, self.settings.mouse_logs_mode, self.settings.mouse_path_shrink)
                
                if self.using_proxy:
                    logger.header('Using Proxy')
                    self.browser.crdi.get('https://browserleaks.com/ip') # pyright: reportUnknownMemberType=false
                    logger.log(f'Check proxy')
                    logger.log(f'Login: {self.settings.proxy_login}')
                    logger.log(f'Password: {self.settings.proxy_pass}')
                    logger.log('Press Enter to continue, or type q to quit')
                    choice = input()
                    if choice.lower() == 'q':
                        return
                
                if self.first_launch:
                    self.first_launch = False
                    logger.header('First Launch')
                    self.browser.crdi.get('https://chrome.google.com/webstore/detail/webrtc-leak-prevent/eiadekoaikejlgdbkbdfeijglgfdalml')
                    logger.log('1) Install extension')
                    logger.log('2) Set last option (IP handling policy: Disable non-proxied UDP (force proxy))')
                    logger.log('3) Close extension settings modal')
                    logger.log('4) Close extension settings chrome tab')
                    logger.log('Press Enter to continue, or type q to quit')
                    choice = input()
                    if choice.lower() == 'q':
                        return
                
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
                
             
        self.control.set_current_action('stopped')   
        # logger.log('Press Enter to close Bot')
        # input()
