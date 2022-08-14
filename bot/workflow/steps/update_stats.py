import requests
import urllib.parse

from .. import Workflow
from ..  import bet365

from ... import logger
from ...errors import BotError


def update_stats(self: Workflow) -> None:
    balance = bet365.get_balance(self.browser)
    unsettled_bets_count = bet365.get_unsettled_bets_count(self.browser)
    
    logger.log(f'Updating stats... ', end_line=False)

    try:
        query_data = {
            'api[method]': 'get_forks',
            'api[version]': '2',
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
            'data[dont_get_forks]': '1',
        }
        bets_request_url = f'http://bvb.strike.ws/bot/index.php?{query_string}'
        logger.log(bets_request_url)
        response = requests.post(bets_request_url, files=request_data, timeout=65)
    except requests.Timeout:
        raise BotError('Request timeout')

    try:
        json = response.json()
    except requests.exceptions.JSONDecodeError:
        logger.log(f'\n{response.text}')
        raise BotError('Invalid JSON in response')

    logger.log(json)