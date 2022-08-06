import re

from typing import Union

from ...browser import Browser
from ...errors import BotError


parameter_selector = '.bss-NormalBetItem_Handicap'

def get_parameter(browser: Browser) -> Union[float, None]:
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
    raise BotError(f'Cannot parse parameter: {parameter_text}')
