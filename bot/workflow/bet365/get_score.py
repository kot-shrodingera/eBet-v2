from typing import Tuple

from ...browser import Browser
from ...errors import BotError, ErrorType

first_score_selector = '.lsb-ScoreBasedScoreboardAggregate_TeamScoreContainer:nth-child(1), .sbm-SoccerGridColumn_IGoal .sbm-SoccerGridCell:nth-child(2)'
second_score_selector = '.lsb-ScoreBasedScoreboardAggregate_TeamScoreContainer:nth-child(2), .sbm-SoccerGridColumn_IGoal .sbm-SoccerGridCell:nth-child(3)'

def get_score(browser: Browser) -> Tuple[int, int]:
    first_score = browser.node('First Score', first_score_selector, 0)
    first_score_text = first_score.get_property('textContent')
    if not first_score_text.isnumeric():
        raise BotError(f'Cannot parse first score: {first_score_text}', ErrorType.CANNOT_PARSE_SCORE)
    
    second_score = browser.node('Second Score', second_score_selector, 0)
    second_score_text = second_score.get_property('textContent')
    if not second_score_text.isnumeric():
        raise BotError(f'Cannot parse second score: {second_score_text}', ErrorType.CANNOT_PARSE_SCORE)
    
    return (int(first_score_text), int(second_score_text))
