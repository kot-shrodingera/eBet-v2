import urllib.parse
import requests

from .. import Workflow


def send_placed_bet(self: Workflow) -> None:
    
    query_data = {
        'api[method]': 'add_placed_bet_to_history',
        'api[version]': '1',
        'bot_version': self.bot_version,
    }
    query_string = urllib.parse.urlencode(query_data)
    json = {
        'bet': self.target_bet,
        'bet365_username': self.settings.username,
        'token': self.ebet_auth_token,
        'balance_before_place_bet': self.balance_before_place_bet['balance'],
        'currency': self.balance_before_place_bet['currency'],
        'bet_amount_initial': self.target_stake_value,
        'bet_amount_result': self.result_stake_value,
        'coefficient_initial': self.initial_coefficient,
        'coefficient_result': self.result_coefficient,
        'parameter_initial': self.initial_parameter,
        'parameter_result': self.result_parameter,
        'bet_open_duration': self.bet_open_duration.total_seconds(),
        'bet_accept_duration': self.bet_accept_duration.total_seconds(),
        'bet_full_duration': self.bet_full_duration.total_seconds(),
        'bot_version': self.bot_version,
        'traders_accepted_amount': self.traders_accepted_amount
    }
    requests.post(f'http://bvb.strike.ws/_router.php?{query_string}', json=json)