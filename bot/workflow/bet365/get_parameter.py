import re

from typing import Optional

from ...browser import Browser
from ...errors import BotError, ErrorType


bet_name_selector = '.bss-NormalBetItem_Title'
parameter_selector = '.bss-NormalBetItem_Handicap'

def get_parameter(browser: Browser) -> Optional[float]:
    bet_name = browser.node('Bet Name', bet_name_selector, 500)
    bet_name_text = bet_name.get_property('textContent').strip()
    
    # TODO: add market checks?
    next_goal_parameter_regex = rf'to score (\d+)(?:st|nd|rd|th) goal$'
    next_goal_parameter_match = re.search(next_goal_parameter_regex, bet_name_text)
    if next_goal_parameter_match:
        return float(next_goal_parameter_match[1])
    
    parameter = browser.node('Parameter', parameter_selector, 500, required=False)
    if not parameter:
        return None
    parameter_text = parameter.get_property('textContent').strip()
    parameter_regex = rf'^([-+]?\d+(\.\d+)?)$'
    parameter_match = re.search(parameter_regex, parameter_text)
    if parameter_match:
        return float(parameter_match[1])
    
    double_parameter_regex = rf'^([-+]?\d+\.\d+),([-+]?\d+\.\d+)$'
    double_parameter_match = re.search(double_parameter_regex, parameter_text)
    if double_parameter_match:
        first_parameter = float(double_parameter_match[1])
        second_parameter = float(double_parameter_match[2])
        return (first_parameter + second_parameter) / 2
    raise BotError(f'Cannot parse parameter: {parameter_text}', ErrorType.CANNOT_PARSE_PARAMETER)
