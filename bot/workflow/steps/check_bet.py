from .. import Workflow, bet365

from ... import logger
from ...errors import BotError


def check_bet(self: Workflow, initial: bool = False) -> None:
    minimum_coefficient = self.bet_details['minimum_coefficient']
    maximum_coefficient = self.bet_details['maximum_coefficient']

    target_parameter = self.bet_details['parameter']
    
    if 'score1' not in self.target_bet:
        raise BotError('No score1 in target bet')
    target_score1 = self.target_bet['score1']
    if not target_score1.isnumeric():
        raise BotError(f'score1 in target bet is not numeric: {target_score1}')
    if 'score2' not in self.target_bet:
        raise BotError('No score2 in target bet')
    target_score2 = self.target_bet['score2']
    if not target_score2.isnumeric():
        raise BotError(f'score2 in target bet is not numeric: {target_score2}')

    logger.log(f'Minimum coefficient: {minimum_coefficient} | Maximum coefficient: {maximum_coefficient} | Target parameter: {target_parameter} | Target Score: {target_score1}-{target_score2}')

    current_balance = bet365.get_balance(self.browser)
    if initial:
        self.balance_before_place_bet = bet365.get_balance(self.browser)
    
    current_coefficient = bet365.get_coefficient(self.browser)
    if initial:
        self.initial_coefficient = current_coefficient

    current_parameter = bet365.get_parameter(self.browser)
    if initial:
        self.initial_parameter = current_parameter

    first_score, second_score = bet365.get_score(self.browser)
    
    logger.log(f'Balance: {current_balance["balance"]} | Coefficient: {current_coefficient} | Parameter: {current_parameter} | Score: {first_score}-{second_score}')
    
    if current_balance['balance'] < self.target_stake_value:
        raise BotError('Balance is less than target stake value')
    
    if current_coefficient < minimum_coefficient:
        raise BotError('Current coefficient is lower than minimum')

    if maximum_coefficient != None and current_coefficient > maximum_coefficient:
        raise BotError('Current coefficient is higher than maximum')
        
    if current_parameter != target_parameter:
        raise BotError('Parameter has changed')
    
    if first_score != int(target_score1) or second_score != int(target_score2):
        raise BotError(f'Not target score {target_score1}-{target_score2}')
