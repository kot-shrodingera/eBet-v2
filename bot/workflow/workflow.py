import urllib.parse
import os.path
import json
import traceback

from typing import Tuple, Union, Dict
from datetime import datetime, timedelta
from time import sleep

from .classes import PlacedBets, BetDetails
from . import bet365

from .. import logger
from ..settings import Settings
from ..browser import Browser, cr_exceptions
from ..errors import BotError
from ..control import Control


class Workflow:
    settings: Settings
    browser: Browser
    control: Control
    bot_version: str
    
    bet365_url_parsed: urllib.parse.SplitResult
    bet365_inplay_url: str
    bet365_my_bets_url: str

    ebet_auth_token: str

    placed_bets_path = './logs/placed_bets.json'
    placed_bets: PlacedBets = {
        'count': 0,
        'events': {}
    }
    last_bet: Union[Dict[str, str], None] = None
    warm_up: bool = False
    warm_up_bets_count: int = 0

    target_bet: Dict[str, str]
    bet_details: BetDetails

    initial_coefficient: float
    initial_parameter: Union[float, None]
    balance_before_place_bet: bet365.Balance
    target_stake_value: float
    
    result_coefficient: float
    result_parameter: Union[float, None]
    
    bot_start_time: datetime
    start_time: datetime
    open_bet_start: datetime
    place_bet_start: datetime
    bet_placed_time: Union[datetime, None] = None
    
    bet_open_duration: timedelta
    bet_accept_duration: timedelta
    bet_full_duration: timedelta
    
    bot_placed_bets_count: int
    bot_bet_tries_count: int
    
    placed_bets_count: int = 0
    bet_tries_count: int = 0
    
    porez = False
    restrict = False
    
    def __init__(self, settings: Settings, ebet_auth_token:str, browser: Browser, control: Control, bot_version: str, bot_start_time: datetime, bot_placed_bets_count: int, bot_bet_tries_count: int) -> None:
        self.settings = settings
        self.browser = browser
        self.control = control
        self.bot_version = bot_version
        
        self.bot_start_time = bot_start_time
        self.start_time = datetime.now()
        
        self.bot_placed_bets_count = bot_placed_bets_count
        self.bot_bet_tries_count = bot_bet_tries_count
        
        self.bet365_url_parsed = urllib.parse.urlsplit(self.settings.bet365_url)
        self.bet365_inplay_url = urllib.parse.urlunsplit(self.bet365_url_parsed._replace(path='#/IP/B1'))
        self.bet365_my_bets_url = urllib.parse.urlunsplit(self.bet365_url_parsed._replace(path='#/MB/'))
        
        self.ebet_auth_token = ebet_auth_token
        
        if os.path.exists(self.placed_bets_path):
            with open(self.placed_bets_path, 'r') as placed_bets_file:
                self.placed_bets = json.loads(placed_bets_file.read())

    def run(self) -> Union[bool, Tuple[int, int]]: # result is need_restart
        from . import steps

        while True:
            try:
                if (self.porez and not self.settings.dont_pause_on_porez) or self.restrict:
                    self.control.set_current_action('pause')
    
                current_action = self.control.get_current_action()
                logger.log(f'Control: {current_action}')
                
                if current_action == 'pause':
                    self.control.set_current_action('paused')
                    sleep(1)
                    seconds_pass = 0
                    while self.control.get_current_action() == 'paused':
                        seconds_pass += 1
                        if seconds_pass > 60:
                            steps.update_stats(self)
                            seconds_pass = 0
                        sleep(1)
                elif current_action == 'init':
                    try:
                        steps.initialize(self)
                        logger.write_log(self.bet_tries_count)
                        self.control.set_current_action('running')
                    except:
                        logger.log('Error while initializing')
                        logger.log(traceback.format_exc())
                        return (self.placed_bets_count, self.bet_tries_count)
                elif current_action == 'running':
                    self.bet_tries_count += 1
                
                    bot_work_time = datetime.now() - self.bot_start_time
                    seconds = bot_work_time.seconds
                    hours = seconds // 3600 + 24 * bot_work_time.days
                    seconds = seconds - (hours * 3600)
                    minutes = seconds // 60
                    seconds = seconds - (minutes * 60)
                    bot_work_time_string = f'{hours:02}:{minutes:02}:{seconds:02}'
                    
                    workflow_work_time = datetime.now() - self.start_time
                    seconds = workflow_work_time.seconds
                    hours = seconds // 3600 + 24 * workflow_work_time.days
                    seconds = seconds - (hours * 3600)
                    minutes = seconds // 60
                    seconds = seconds - (minutes * 60)
                    workflow_work_time_string = f'{hours:02}:{minutes:02}:{seconds:02}'
                    
                    if self.warm_up:
                        logger.header(f'Bet Try №{self.bet_tries_count} (Warm Up: {self.warm_up_bets_count} of {self.settings.warm_up_bets_limit}) ({workflow_work_time_string}|{bot_work_time_string})')
                    else:
                        logger.header(f'Bet Try №{self.bet_tries_count}|{self.bot_bet_tries_count + self.bet_tries_count} (Placed bets: {self.placed_bets_count}|{self.bot_placed_bets_count + self.placed_bets_count}) ({workflow_work_time_string}|{bot_work_time_string})')
                    
                    steps.authorize(self)
                    
                    steps.clear_betslip(self)
                    
                    steps.set_target_bet(self)
                    if not self.target_bet:
                        continue
                    
                    current_balance = bet365.get_balance(self.browser)
                    if current_balance['balance'] < self.settings.stake:
                        raise BotError('Balance is less than stake')
                    
                    steps.open_event(self)
                    
                    steps.open_selection(self)
                    
                    if self.warm_up:
                        self.warm_up_bets_count += 1
                        logger.log(f'Warm Up bet openned ({self.warm_up_bets_count} of {self.settings.warm_up_bets_limit})')
                        sleep(1)
                        steps.clear_betslip(self)
                        continue
                    
                    steps.set_stake_value(self)
                    
                    steps.set_balance_before_place_bet(self)
                    
                    steps.check_bet(self, initial=True)
                    
                    if self.settings.dont_place_bets:
                        logger.log('Bet placing disabled')
                        continue
                    
                    if steps.place_bet(self):
                        delay = self.settings.placed_bet_to_new_try_delay
                        if delay and delay > 0:
                            logger.log(f'Waiting {delay} seconds')
                            sleep(delay)
                    else:
                        sleep(1)
                elif current_action == 'stop':
                    return False
                else:
                    logger.log(f'Unknown action: {current_action}')
                    while current_action == self.control.get_current_action():
                        sleep(1)
                
            except BotError as error:
                logger.log(f'[ERROR]: {str(error)}')
            except (cr_exceptions.ChromeCommunicationsError, ConnectionAbortedError, AssertionError):
                logger.log('Chrome Died')
                logger.log(traceback.format_exc())
                logger.write_log(self.bet_tries_count)
                return (self.placed_bets_count, self.bet_tries_count)
            except Exception:
                logger.log(traceback.format_exc())
            finally:
                logger.write_log(self.bet_tries_count)
                if self.settings.placed_bets_limit and self.placed_bets_count >= self.settings.placed_bets_limit:
                    logger.log('Placed Bets Limit has been reached. Pausing')
                    self.control.set_current_action('pause')
                elif self.settings.browser_restart_interval is not None and (datetime.now() - self.start_time).seconds > self.settings.browser_restart_interval:
                    return (self.placed_bets_count, self.bet_tries_count)
