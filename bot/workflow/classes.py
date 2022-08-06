from typing import TypedDict, Dict, Union


class Bet(TypedDict):
    bk_id_std: str
    bet365_bet_name: str
    bet_unique_key: str


class PlacedUnique(TypedDict):
    count: int

class PlacedSelection(TypedDict):
    count: int
    unique: Dict[str, PlacedUnique]

class PlacedEvent(TypedDict):
    name: str
    count: int
    selections: Dict[str, PlacedSelection]

class PlacedBets(TypedDict):
    count: int
    events: Dict[str, PlacedEvent]


class BetDetails(TypedDict):
    match_link: str
    market: str
    selection: str
    alternative_selection_name: Union[str, None]
    column: Union[str, None]
    minimum_coefficient: float
    parameter: Union[float, None]
