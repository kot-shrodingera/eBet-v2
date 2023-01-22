from __future__ import annotations

from .. import Workflow

def get_placed_bets_keys(self: Workflow) -> dict[str, list[str]]:
    placed_bets = self.placed_bets
    result: dict[str, list[str]] = {}
    
    for event_id, event in self.placed_bets['events'].items():
        result[event_id] = []
        event = self.placed_bets['events'][event_id]
        for selection in event['selections'].values():
            for unique_key in selection['unique'].keys():
                result[event_id].append(unique_key)
    
    return result