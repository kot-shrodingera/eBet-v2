from .. import Workflow, bet365

from ... import logger
from ...errors import BotError


def check_bet(self: Workflow, initial: bool = False) -> None:
    minimum_coefficient = self.bet_details['minimum_coefficient']
    current_coefficient = bet365.get_coefficient(self.browser)
    if initial:
        self.initial_coefficient = current_coefficient

    target_parameter = self.bet_details['parameter']
    current_parameter = bet365.get_parameter(self.browser)
    if initial:
        self.initial_parameter = current_parameter

    current_balance = bet365.get_balance(self.browser)
    if initial:
        self.balance_before_place_bet = bet365.get_balance(self.browser)
    
    logger.log(f'Balance: {current_balance["balance"]} | Coefficient: {current_coefficient} | Parameter: {current_parameter}')
    
    if current_coefficient < minimum_coefficient:
        raise BotError('Current coefficient is lower than minimum')
    if current_parameter != target_parameter:
        raise BotError('Parameter has changed')
    if current_balance['balance'] < self.settings.stake:
        raise BotError('Balance is less than stake')
