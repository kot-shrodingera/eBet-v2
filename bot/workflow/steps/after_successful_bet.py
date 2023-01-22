import json
import datetime

from .. import Workflow, bet365, steps

from ... import logger


def after_successful_bet(self: Workflow) -> None:
    self.bet_placed_time = datetime.datetime.now()
    self.bet_open_duration = self.place_bet_start - self.open_bet_start
    self.bet_accept_duration = self.bet_placed_time - self.place_bet_start
    self.bet_full_duration = self.bet_placed_time - self.open_bet_start
    
    self.result_coefficient = bet365.get_coefficient(self.browser)
    logger.log(f'Result Coefficient: {self.result_coefficient}')
    self.result_parameter = bet365.get_parameter(self.browser)
    logger.log(f'Result Parameter: {self.result_parameter}')
    self.result_stake_value = bet365.get_result_stake_value(self.browser)
    logger.log(f'Result Stake Value: {self.result_stake_value}')
    
    steps.clear_old_placed_bets(self)
    
    steps.update_placed_bets(self)
    
    steps.send_placed_bet(self)

    with open(self.placed_bets_path, 'w', encoding='utf-8') as placed_bets_file:
        placed_bets_file.write(json.dumps(self.placed_bets, indent=2))
