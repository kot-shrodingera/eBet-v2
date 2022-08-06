from time import sleep

from .. import Workflow

from ... import logger


clear_betslip_button_selector = '.bss-RemoveButton, .bss-ReceiptContent_Done'

def clear_betslip(self: Workflow) -> None:
    # logger.log('Checking Betslip Clear')
    clear_betslip_button = self.browser.node('Clear Betslip Button', clear_betslip_button_selector, 1, required=False)
    if not clear_betslip_button:
        logger.log('No Betslip Opened')
        return
    logger.log('Clearing Betslip')
    clear_betslip_button.click()
    
    sleep(0.5)
