from .. import Workflow, bet365

from ... import logger
from ...errors import BotError, ErrorType


def check_bet_name(self: Workflow) -> None:
    target_market_name = self.bet_details['market']
    target_bet_name = self.bet_details['selection']

    bet_name = bet365.get_bet_name(self.browser)
    market_name = bet365.get_market_name(self.browser)
    
    logger.log(f'Target market: {target_market_name} | Target bet name: {target_bet_name}')
    logger.log(f'Opened market: {market_name} | Opened bet name: {bet_name}')
    
    ok = True
    if target_market_name != market_name:
        if self.settings.strict_bet_name_check:
            raise BotError('Wrong market name', ErrorType.WRONG_BET_OPENED)
        else:
            logger.log('Wrong market name')
        ok = False
    if target_bet_name != bet_name:
        if self.settings.strict_bet_name_check:
            raise BotError('Wrong bet name', ErrorType.WRONG_BET_OPENED)
        else:
            logger.log('Wrong bet name')
        ok = False
    
    if ok:
        logger.log('Market and bet name OK')
