from ..bet365.get_balance import get_balance
from ..bet365.get_stake_value import get_stake_value
from .. import Workflow

from ... import logger
from ...errors import BotError

def calculate_stake_value(self: Workflow) -> None:
    if self.settings.stake_type == 'fixed':
        base_target_stake_value = self.settings.stake
    elif self.settings.stake_type == 'percent':
        balance = get_balance(self.browser)
        percent_stake = round(balance['balance'] * self.settings.stake / 100, 2)
        logger.log(f'Percent stake is {percent_stake}')
        if self.settings.stake_max is None:
            logger.log('No Maximum stake')
            base_target_stake_value = round(balance['balance'] * self.settings.stake / 100, 2)
        else:
            logger.log(f'Maximum stake is {self.settings.stake_max}')
            base_target_stake_value = min(round(balance['balance'] * self.settings.stake / 100, 2), self.settings.stake_max)
    else:
        raise BotError(f'Unknown stake type: {self.settings.stake_type}')
    
    if 'stake_sum_multiplier' in self.target_bet:
        stake_sum_multiplier = float(self.target_bet['stake_sum_multiplier'])
        self.target_stake_value = round(stake_sum_multiplier * base_target_stake_value, 2)
        logger.log(f'Target Stake Value ({stake_sum_multiplier} * {base_target_stake_value} = {self.target_stake_value})')
    else:
        self.target_stake_value = base_target_stake_value
        logger.log(f'Target Stake Value ({self.target_stake_value})')
