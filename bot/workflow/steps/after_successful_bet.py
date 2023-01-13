import json

from datetime import datetime

from .send_placed_bet import send_placed_bet

from .. import Workflow, bet365

from ... import logger
from ...errors import BotError


def after_successful_bet(self: Workflow) -> None:
    self.bet_placed_time = datetime.now()
    self.bet_open_duration = self.place_bet_start - self.open_bet_start
    self.bet_accept_duration = self.bet_placed_time - self.place_bet_start
    self.bet_full_duration = self.bet_placed_time - self.open_bet_start
    
    self.result_coefficient = bet365.get_coefficient(self.browser)
    logger.log(f'Result Coefficient: {self.result_coefficient}')
    self.result_parameter = bet365.get_parameter(self.browser)
    logger.log(f'Result Parameter: {self.result_parameter}')
    self.result_stake_value = bet365.get_result_stake_value(self.browser)
    logger.log(f'Result Stake Value: {self.result_stake_value}')
    
    assert(self.target_bet)
    
    bk_id_std = self.target_bet['bk_id_std']
    bet_name = self.target_bet['bet365_bet_name']
    bet_unique_key = self.target_bet['bot_bet_unique_key']
    
    self.placed_bets_count += 1
    
    self.placed_bets['count'] += 1

    placed_events = self.placed_bets['events']
    if bk_id_std not in placed_events:
        placed_events[bk_id_std] = {
            'name': self.target_bet['event'],
            'count': 1,
            'selections': {},
        }
    else:
        placed_events[bk_id_std]['count'] += 1

    placed_selections = placed_events[bk_id_std]['selections']
    if bet_name not in placed_selections:
        placed_selections[bet_name] = {
            'count': 1,
            'unique': {},
        }
    else:
        placed_selections[bet_name]['count'] += 1

    placed_unique = placed_selections[bet_name]['unique']
    if bet_unique_key not in placed_unique:
        placed_unique[bet_unique_key] = {
            'count': 1,
        }
    else:
        placed_unique[bet_unique_key]['count'] += 1

    send_placed_bet(self)
    with open(self.placed_bets_path, 'w', encoding='utf-8') as placed_bets_file:
        placed_bets_file.write(json.dumps(self.placed_bets, indent=2))
