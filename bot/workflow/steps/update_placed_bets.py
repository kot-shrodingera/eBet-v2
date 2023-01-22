import datetime

from .. import Workflow


def update_placed_bets(self: Workflow) -> None:
    assert(self.target_bet)
    
    bk_id_std = self.target_bet['bk_id_std']
    bet_name = self.target_bet['bet365_bet_name']
    bot_bet_unique_key = self.target_bet['bot_bet_unique_key']
    
    self.placed_bets_count += 1
    
    self.placed_bets['count'] += 1

    placed_events = self.placed_bets['events']
    if bk_id_std not in placed_events:
        placed_events[bk_id_std] = {
            'name': self.target_bet['event'],
            'count': 1,
            'selections': {},
        }
    else:
        placed_events[bk_id_std]['count'] += 1

    placed_selections = placed_events[bk_id_std]['selections']
    if bet_name not in placed_selections:
        placed_selections[bet_name] = {
            'count': 1,
            'unique': {},
        }
    else:
        placed_selections[bet_name]['count'] += 1

    placed_unique = placed_selections[bet_name]['unique']
    placed_unique[bot_bet_unique_key] = {
        'timestamp': datetime.datetime.now().isoformat()
    }
