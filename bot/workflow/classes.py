from typing import TypedDict, Optional, Dict

# data in bets response
class Bet(TypedDict):
    id: str
    bet_hash_in_history: str
    created_at: str
    pm_live: str
    strategy_num: str
    bk_id_std: str
    league: str
    league_id: str
    event: str
    duration: str
    duration_sec: str
    team1: str
    player1: str
    team2: str
    player2: str
    score1: str
    score2: str
    period: str
    bet_type: str
    bet: str
    bet_unique_key: str
    param: Optional[str]
    coef: str
    meta: str
    direct_link: str
    time_from_score_change: str
    time_from_score1_change: str
    time_from_score2_change: str
    strd_player_strength: str
    strd_prematch_data_duration_sec: str
    strd_max_time_from_score_change: str
    max_lower_coef_percent: float
    max_upper_coef_percent: float
    pms_period: str
    pms_market: str
    pms_selection: str
    stake_sum_multiplier: float
    bet365_bet_name: str
    bet365_direct_link: str
    request_bets_hash: str


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

# period:
#     FULLTIME
#     1 HALF
#     2 HALF

# selection(все варианты):
#     WIN1
#     DRAW
#     WIN2
#     WIN1 OR DRAW
#     WIN2 OR DRAW
#     WIN1 OR WIN2
#     OVER
#     UNDER

# market:
#     RESULT
#         WIN1
#         DRAW
#         WIN2
#     DOUBLE CHANCE
#         WIN1 OR DRAW
#         WIN2 OR DRAW
#         WIN1 OR WIN2
#     TOTAL
#         OVER
#         UNDER
#     T1 TOTAL
#         OVER
#         UNDER
#     T2 TOTAL
#         OVER
#         UNDER
#     3W HANDICAP
#         WIN1
#         DRAW
#         WIN2

class CouponValidationData(TypedDict):
    period: str
    market: str
    selection: str

class BetDetails(TypedDict):
    match_link: str
    market: str
    selection: str
    alternative_selection_name: Optional[str]
    column: Optional[str]
    minimum_coefficient: float
    maximum_coefficient: Optional[float]
    parameter: Optional[float]
    coupon_validation_data: CouponValidationData
    team1: str
    team2: str
