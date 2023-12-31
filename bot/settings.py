import os
import json

from configparser import ConfigParser
from typing import Optional, Union, Type


class Settings:
    api_key: str
    api_password: str
    username: str
    password: str
    chrome_binary_path: str
    chrome_port: int
    
    bet365_url: str
    stake: float
    stake_type: str
    stake_min: float
    stake_max: Optional[float]
    
    max_same_bets_count: int
    max_event_bets_count: int
    warm_up_bets_limit: Optional[int]
    history_limit_minutes: int
    
    placed_bet_to_new_try_delay: Optional[float]
    placed_bet_to_open_delay: Optional[float]
    placed_bet_to_place_delay: Optional[float]
    
    close_page_on_placed_bet: bool
    browser_restart_interval: Optional[int]
    mouse_path_shrink: float
    dont_pause_stream: bool
    strict_bet_name_check: bool
    disable_refresh_balance: bool
    js_refresh_balance: bool
    show_click_coords: bool
    narrow_click_coords: float
    js_scroll: bool
    use_bet_credits: bool
    open_tries_limit: int
    find_tries_limit: int
    open_coupon_wait_time: int
    
    window_width: Optional[int]
    window_height: Optional[int]
    placed_bets_limit: Optional[int]
    request_all_bets: bool
    dont_place_bets: bool
    dont_pause_on_porez: bool
    bets_request_timeout: Optional[int]
    dev: bool

    def __init__(self, settings_file_name: str) -> None:
        settings = ConfigParser()
        settings.read(settings_file_name)
        
        def set_property(property: str, config_path: str, type: Union[Type[str], Type[int], Type[float], Type[bool]] = str, default: Union[str, int, float, bool, None] = None, required: bool = True):
            if config_path not in settings['Settings'] or settings['Settings'][config_path] == '':
                if default != None:
                    # print(f'No {config_path} in settings file. Using default {default}')
                    setattr(self, property, default)
                elif not required:
                    setattr(self, property, None)
                else:
                    raise Exception(f'No {config_path} in settings file')
            else:
                value = None
                if type == str:
                    value = settings['Settings'][config_path]
                elif type == int:
                    try:
                        value = int(settings['Settings'][config_path])
                    except ValueError:
                        raise Exception(f'{property} in settings file is not int')
                elif type == float:
                    try:
                        value = float(settings['Settings'][config_path])
                    except ValueError:
                        raise Exception(f'{property} in settings file is not float')
                elif type == bool:
                    value = settings.getboolean('Settings', config_path)
                    
                setattr(self, property, value)

        set_property('api_key', 'api_key')
        set_property('api_password', 'api_password')
        set_property('username', 'username')
        set_property('password', 'password')
        set_property('chrome_port', 'chrome_port', int, default=9222)
        
        set_property('bet365_url', 'bet365_url', default='https://www.bet365.com/') # TODO: URL validation
        set_property('stake', 'stake', float)
        set_property('stake_type', 'stake_type', default='fixed') # TODO: validation ['fixed', 'percent']
        set_property('stake_min', 'stake_min', float, default=0.2)
        set_property('stake_max', 'stake_max', float, required=False)
        
        set_property('max_same_bets_count', 'max_same_bets_count', int)
        set_property('max_event_bets_count', 'max_event_bets_count', int)
        set_property('warm_up_bets_limit', 'warm_up_bets_limit', int, required=False)
        set_property('history_limit_minutes', 'history_limit_minutes', int, default=20)
        
        set_property('placed_bet_to_new_try_delay', 'placed_bet_to_new_try_delay', float, required=False)
        set_property('placed_bet_to_open_delay', 'placed_bet_to_open_delay', float, required=False)
        set_property('placed_bet_to_place_delay', 'placed_bet_to_place_delay', float, required=False)
        
        set_property('close_page_on_placed_bet', 'close_page_on_placed_bet', bool, default=False)
        set_property('browser_restart_interval', 'browser_restart_interval', int, required=False)
        set_property('mouse_path_shrink', 'mouse_path_shrink', float, default=1) # TODO: validate [0.0 - 1.0]
        set_property('dont_pause_stream', 'dont_pause_stream', bool, default=False)
        set_property('strict_bet_name_check', 'strict_bet_name_check', bool, default=False)
        set_property('disable_refresh_balance', 'disable_refresh_balance', bool, default=False)
        set_property('js_refresh_balance', 'js_refresh_balance', bool, default=False)
        set_property('show_click_coords', 'show_click_coords', bool, default=False)
        set_property('narrow_click_coords', 'narrow_click_coords', float, default=1) # TODO: validate [0.0 - 1.0]
        set_property('js_scroll', 'js_scroll', bool, default=False)
        set_property('use_bet_credits', 'use_bet_credits', bool, default=False)
        set_property('open_tries_limit', 'open_tries_limit', int, default=5)
        set_property('find_tries_limit', 'find_tries_limit', int, default=10)
        set_property('open_coupon_wait_time', 'open_coupon_wait_time', int, default=1000)
        
        set_property('window_width', 'window_width', int, required=False)
        set_property('window_height', 'window_height', int, required=False)
        set_property('placed_bets_limit', 'placed_bets_limit', int, required=False)
        set_property('request_all_bets', 'request_all_bets', bool, default=False)
        set_property('dont_place_bets', 'dont_place_bets', bool, default=False)
        set_property('dont_pause_on_porez', 'dont_pause_on_porez', bool, default=False)
        set_property('bets_request_timeout', 'bets_request_timeout', int, required=False)
        set_property('dev', 'dev', bool, default=False)
        
        if not 'chrome_binary_path' in settings['Settings']:
            standard_paths = [
                'C:/Program Files/Google/Chrome/Application/chrome.exe',
                'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
            ]
            try:
                self.chrome_binary_path = next(path for path in standard_paths if os.path.exists(path))
            except StopIteration:
                raise Exception('No chrome_binary_path in settings file, and cannot find it in standart paths')
        else:
            self.chrome_binary_path = settings['Settings']['chrome_binary_path']
            if not os.path.exists(self.chrome_binary_path):
                raise Exception(f'Chrome executable not exists: {self.chrome_binary_path}')
    
    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=2)
        