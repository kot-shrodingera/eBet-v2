from time import sleep

from .authorize import authorize
from .clear_betslip import clear_betslip

from .. import Workflow

from ... import logger

def initialize(self: Workflow) -> None:
    logger.header('Initialize')
    self.browser.crdi.get(self.bet365_inplay_url) # pyright: reportUnknownMemberType=false
    logger.log('Bet365 tab opened')

    self.browser.create_isolated_world()
    sleep(0.25)
    authorize(self)
    
    clear_betslip(self)
