from .. import Workflow, bet365

from ... import logger
from ...errors import BotError, ErrorType

def calculate_stake_value(self: Workflow) -> None:
    if self.settings.stake_type == 'fixed':
        base_target_stake_value = self.settings.stake
        logger.log(f'Base Target Stake Value (fixed): {base_target_stake_value}')
    elif self.settings.stake_type == 'percent':
        balance = bet365.get_balance(self.browser)
        base_target_stake_value = round(balance['balance'] * self.settings.stake / 100, 2)
        logger.log(f'Base Target Stake Value (percent): {balance["balance"]} * {self.settings.stake / 100} = {base_target_stake_value}')
    elif self.settings.stake_type == 'fixed_win':
        balance = bet365.get_balance(self.browser)
        current_coefficient = bet365.get_coefficient(self.browser)
        base_target_stake_value = round(self.settings.stake / (current_coefficient - 1), 2)
        logger.log(f'Base Target Stake Value (fixed_win): {self.settings.stake} / ({current_coefficient} - 1) = {base_target_stake_value}')
    elif self.settings.stake_type == 'percent_win':
        balance = bet365.get_balance(self.browser)
        target_win = round(balance['balance'] * self.settings.stake / 100, 2)
        logger.log(f'Target Win (percent_win): {balance["balance"]} * {self.settings.stake / 100} = {target_win}')
        current_coefficient = bet365.get_coefficient(self.browser)
        base_target_stake_value = round(target_win / (current_coefficient - 1), 2)
        logger.log(f'Base Target Stake Value (percent_win): {target_win} / ({current_coefficient} - 1 = {base_target_stake_value}')
    else:
        raise BotError(f'Unknown stake type: {self.settings.stake_type}', ErrorType.UNKNOWN_STAKE_TYPE_IN_SETTINGS)
    
    if self.settings.stake_max is None:
        logger.log('No Maximum stake')
    else:
        logger.log(f'Maximum stake is {self.settings.stake_max}')
        if self.settings.stake_max < base_target_stake_value:
            logger.log('Base Target Stake Value is higher than maximum')
            base_target_stake_value = self.settings.stake_max
    
    assert(self.target_bet)
    
    if 'stake_sum_multiplier' in self.target_bet:
        stake_sum_multiplier = float(self.target_bet['stake_sum_multiplier'])
        new_target_stake_value = round(stake_sum_multiplier * base_target_stake_value, 2)
        logger.log(f'Stake Sum Multiplier: {stake_sum_multiplier} * {base_target_stake_value} = {new_target_stake_value}')
        base_target_stake_value = new_target_stake_value
    
    balance = bet365.get_balance(self.browser)
    if balance['balance'] < base_target_stake_value:
        logger.log('Balance is less than target stake value')
        base_target_stake_value = balance['balance']
    
    if base_target_stake_value < self.settings.stake_min:
        raise BotError(f'Base Target Stake Value ({base_target_stake_value}) is lower than minimum ({self.settings.stake_min})', ErrorType.UNKNOWN_STAKE_TYPE_IN_SETTINGS)
    
    self.target_stake_value = base_target_stake_value
    logger.log(f'Target Stake Value: {self.target_stake_value}')
