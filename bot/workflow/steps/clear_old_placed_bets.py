import datetime

from .. import Workflow


def clear_old_placed_bets(self: Workflow) -> None:
    now = datetime.datetime.now()
    history_limit_minutes = self.settings.history_limit_minutes
    
    # list() is because of dict element removal which cause "RuntimeError: dictionary changed size during iteration"
    for event_id in list(self.placed_bets['events'].keys()):
        event = self.placed_bets['events'][event_id]
        for selection_id in list(event['selections'].keys()):
            selection = event['selections'][selection_id]
            for unique_key in list(selection['unique'].keys()):
                unique = selection['unique'][unique_key]
                if 'timestamp' in unique:
                    unique_timestamp = unique['timestamp']
                    diff = now - datetime.datetime.fromisoformat(unique_timestamp)
                else:
                    diff = None
                if diff is None or diff.seconds > history_limit_minutes * 60:
                    del selection['unique'][unique_key]
                    selection['count'] -= 1
                    event['count'] -= 1
                    self.placed_bets['count'] -= 1
            if selection['count'] == 0:
                del event['selections'][selection_id]
        if event['count'] == 0:
            del self.placed_bets['events'][event_id]