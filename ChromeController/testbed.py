import os, subprocess
from ChromeController import Chrome
from timeout import random_timeout
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename='testbed.log', mode='w', maxBytes=99999)
log_formatter = logging.Formatter('%(asctime)s (%(levelname)s) %(filename)s %(funcName)s(%(lineno)d): %(message)s')
handler.setFormatter(log_formatter)
logger.addHandler(handler)

# import requests
# try:
#     requests.get('http://localhost:9222/')
# except requests.exceptions.ConnectionError:
#     print('Opening')
#     subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', '--remote-debugging-port=9222'])
#     random_timeout(2)
# quit()

profile = 'C:/Users/Admin/AppData/Local/Google/Chrome/User Data/Default'
profile = os.getcwd() + '/test'
browser = Chrome(profile=profile)
browser.get('https://www.bet365.com/#/IP/B1')
random_timeout(10)
browser.get('https://www.bet365.com/#/IP/EV15773488052C1')
new_tab = browser.new_tab()
new_tab.get('https://www.bet365.com/#/IP/EV15773488052C1')
browser.focus_tab()
browser.get('https://www.bet365.com/#/IP/B1')

# for tab_number in range(1, 250): # Crashes at 21
#     print('Opening tab', tab_number)
#     new_tab = browser.new_tab()
#     random_timeout(1)
#     new_tab.close()
#     random_timeout(1)