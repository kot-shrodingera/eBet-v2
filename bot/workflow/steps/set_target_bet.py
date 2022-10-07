import requests
import urllib.parse

from datetime import datetime

from .. import Workflow
from ..  import bet365
from ..classes import Bet

from ... import logger
from ...errors import BotError


def target_bet_predicate(self: Workflow, bet: Bet) -> bool:
    bk_id_std = bet['bk_id_std']
    bet_name = bet['bet365_bet_name']
    bet_unique_key = bet['bet_unique_key']
    placed_events = self.placed_bets['events']
    if bk_id_std in placed_events:
        placed_event = placed_events[bk_id_std]
        if placed_event['count'] >= self.settings.max_event_bets_count:
            return False
        placed_selections = placed_event['selections']
        if bet_name in placed_selections:
            placed_selection = placed_selections[bet_name]
            if placed_selection['count'] >= self.settings.max_same_bets_count:
                return False
            if bet_unique_key in placed_selection['unique']:
                return False
    return True

def set_target_bet(self: Workflow) -> None:
    balance = bet365.get_balance(self.browser)
    unsettled_bets_count = bet365.get_unsettled_bets_count(self.browser)
    
    self.warm_up = self.settings.warm_up_bets_limit is not None and self.warm_up_bets_count < self.settings.warm_up_bets_limit
    logger.log(f'Bets request{" (Warm Up)" if self.warm_up else ""}... ', end_line=False)

    try:
        query_data = {
            'api[method]': 'get_forks',
            'api[version]': '2',
            'bot_version': self.bot_version,
            'get_progrev_bets': '1' if self.warm_up or self.settings.request_all_bets else '0',
        }
        query_string = urllib.parse.urlencode(query_data)
        request_data = {
            'data[token]': (None, self.ebet_auth_token),
            'data[bk_login]': (None, self.settings.username),
            'data[balance]': (None, str(balance['balance'])),
            # 'data[currency]': (None, balance['currency']),
            'data[unsettled_bets_count]': (None, str(unsettled_bets_count)),
            'data[is_porez]': (None, '1' if self.porez else '0'),
            'data[is_restrict]': (None, '1' if self.restrict else '0'),
        }
        if self.settings.bets_request_timeout:
            request_data['data[timeout]'] = (None, str(self.settings.bets_request_timeout))
        bets_request_url = f'http://bvb.strike.ws/bot/index.php?{query_string}'
        response = requests.post(bets_request_url, files=request_data, timeout=65)
    except requests.Timeout:
        raise BotError('Request timeout')

    try:
        json = response.json()
    except requests.exceptions.JSONDecodeError:
        logger.log(f'\n{response.text}')
        raise BotError('Invalid JSON in response')

    if 'data' not in json or 'forks' not in json['data']:
        logger.log(f'\n{json}')
        raise BotError('Not data.forks in response')
    bets = json['data']['forks']

    logger.log(f'Done (Got {len(bets)} bets)')
    
    self.open_bet_start = datetime.now()
    
    self.target_bet = next(filter(lambda bet: target_bet_predicate(self, bet), bets), {})
    if not self.target_bet:
        logger.log('No matching bets')
        return

    self.bet_details = {
        'match_link': urllib.parse.urlunsplit(self.bet365_url_parsed._replace(path=urllib.parse.urlsplit(self.target_bet['bet365_direct_link'], allow_fragments=False).path)),
        'market': '',
        'selection': '',
        'alternative_selection_name': None,
        'column': None,
        'minimum_coefficient': float(self.target_bet['max_lower_coef_percent']) if 'max_lower_coef_percent' in self.target_bet else 1.1,
        'maximum_coefficient': float(self.target_bet['max_upperr_coef_percent']) if 'max_upperr_coef_percent' in self.target_bet else None,
        'parameter': float(self.target_bet['param']) if 'param' in self.target_bet and self.target_bet['param'] != None else None,
    }
    selection_details = self.target_bet['bet365_bet_name'].split('|')
    if len(selection_details) == 2:
        self.bet_details['market'], self.bet_details['selection'] = selection_details
    elif len(selection_details) == 3:
        self.bet_details['market'], self.bet_details['selection'], self.bet_details['column'] = selection_details
    elif len(selection_details) == 4:
        self.bet_details['market'], self.bet_details['alternative_selection_name'], self.bet_details['column'], self.bet_details['selection'] = selection_details
    else:
        raise BotError(f'Cannot parse selection details: {self.target_bet["bet365_bet_name"]}')
    logger.log(f'Target Bet:')
    logger.log(f'Event: {self.target_bet["event"]}')
    logger.log(f'Selection: {self.bet_details["market"]} | {self.bet_details["selection"]} | {self.bet_details["column"]}')
