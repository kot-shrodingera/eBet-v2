from .. import Workflow, bet365

from ... import logger


def set_balance_before_place_bet(self: Workflow) -> None:      
    self.balance_before_place_bet = bet365.get_balance(self.browser)
    logger.log(f'Balance before place bet: {self.balance_before_place_bet}')
