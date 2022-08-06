from time import sleep

from .. import Workflow

from ... import logger

event_header_selector = '.ipe-EventHeader_Fixture'

def open_event(self: Workflow) -> None:
    logger.log(f'Opening event {self.bet_details["match_link"]}... ', end_line=False)

    # browser.get('chrome://newtab')
    # browser.get(match_link)

    self.browser.go_to_url(self.bet_details["match_link"])
    # browser.Page_navigate(url=self.bet_details['match_link'])
    logger.log('Event opened')

    self.browser.create_isolated_world()
    sleep(0.25)
    # Иногда тут жесткая задержка, хз почему, если после create_isolated_world делать доп задержку, этой тут не будет, при 0.1 она редко

    # browser.wait_for('.ipe-EventHeader_Fixture, .ml1-LocationEventsMenu_Text, .sph-EventHeader') # Wait for match page to load
    self.browser.node('Event Header', event_header_selector)
    
    sleep(0.5)

    # Not needed?
    # browser.scroll_to(container_css_selector='.ipe-EventViewDetailScroller', amount=1) # Scroll once to load all markets
    # if doing scroll must wait some time, otherwise selection clicking can be failed cause of mooving coordinates