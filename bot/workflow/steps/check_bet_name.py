from typing import Optional
from .. import Workflow, bet365

from ... import logger
from ...errors import BotError, ErrorType

# $T1 - Team 1
# $T2 - Team 2
# $P - Parameter (2.5, -1.5)
# $SP - Signed Parameter (+2.5, -1.5)
# $ISP - Inverted Signed Parameter (-2.5, +1.5)
pms_data = {
    'RESULT': {
        'FULLTIME': 'Fulltime Result',
        'selections': {
            'WIN1': '[$T1]',
            'DRAW': 'Draw',
            'WIN2': '[$T2]',
        },
    },
    'DOUBLE CHANCE': {
        'FULLTIME': 'Double Chance',
        'selections': {
            'WIN1 OR DRAW': '[$T1] or Draw',
            'WIN2 OR DRAW': '[$T2] or Draw',
            'WIN1 OR WIN2': '[$T1] or [$T2]',
        },
    },
    'TOTAL': {
        'FULLTIME': 'Match Goals',
        '1 HALF': 'First Half Goals',
        'selections': {
            'OVER': 'Over[$P]',
            'UNDER': 'Under[$P]',
        },
    },
    'T1 TOTAL': {
        'FULLTIME': 'Home Team Goals',
        'selections': {
            'OVER': '[$T1] - Over[$P]',
            'UNDER': '[$T1] - Under[$P]',
        },
    },
    'T2 TOTAL': {
        'FULLTIME': 'Away Team Goals',
        'selections': {
            'OVER': '[$T2] - Over[$P]',
            'UNDER': '[$T2] - Under[$P]',
        },
    },
    '3W HANDICAP': {
        'FULLTIME': '3-Way Handicap',
        'selections': {
            'WIN1': '[$T1][$PZ]',
            'DRAW': 'Draw ([$T2] )[$PZ]',
            'WIN2': '[$T2][$PZ]',
        },
    },
    'ASIAN HANDICAP': {
        'FULLTIME': 'Asian Handicap In-Play',
        'selections': {
            'WIN1': '([$S]) [$T1][$P]',
            'WIN2': '([$S]) [$T2][$P]',
        },
    },
}

def handle_template(template: str, team1: str, team2: str, parameter: Optional[str], score: str) -> str:
    result = template.replace('[$T1]', team1).replace('[$T2]', team2).replace('[$S]', score)
    if '[$P]' in template or '[$PZ]' in template:
        if parameter is None:
            raise BotError(f'Parameter template ({template}) in parameterless bet', ErrorType.PMS_ERROR)
        result = result.replace('[$P]', parameter).replace('[$PZ]', f'{parameter}.0')
    return result
    

def check_bet_name(self: Workflow) -> None:
    pms_period = self.bet_details['coupon_validation_data']['period']
    pms_market = self.bet_details['coupon_validation_data']['market']
    pms_selection = self.bet_details['coupon_validation_data']['selection']
    
    selection_name = bet365.get_selection_name(self.browser)
    market_name = bet365.get_market_name(self.browser)
    
    if pms_market not in pms_data:
        raise BotError(f'Unknown pms market: {pms_market}', ErrorType.PMS_ERROR)
    if pms_period not in pms_data[pms_market]:
        raise BotError(f'Unknown pms period: {pms_market}:{pms_period}', ErrorType.PMS_ERROR)
    if pms_selection not in pms_data[pms_market]['selections']:
        raise BotError(f'Unknown pms selection: {pms_market}:{pms_selection}', ErrorType.PMS_ERROR)
    
    target_coupon_market = pms_data[pms_market][pms_period]
    target_coupon_selection = handle_template(pms_data[pms_market]['selections'][pms_selection], self.bet_details['team1'], self.bet_details['team2'], self.bet_details['bet365_selection_parameter'], self.bet_details['score'])
    
    logger.log(f'Target market: {target_coupon_market} | Target selection: {target_coupon_selection}')
    logger.log(f'Opened market: {market_name} | Opened selection: {selection_name}')
    
    ok = True
    if target_coupon_market != market_name:
        if self.settings.strict_bet_name_check:
            raise BotError('Wrong market name', ErrorType.WRONG_BET_OPENED)
        else:
            logger.log('Wrong market name')
        ok = False
    if target_coupon_selection != selection_name:
        if self.settings.strict_bet_name_check:
            raise BotError('Wrong bet name', ErrorType.WRONG_BET_OPENED)
        else:
            logger.log('Wrong bet name')
        ok = False
    
    if ok:
        logger.log('Market and bet name OK')
