import msvcrt
import os
import urllib.parse
import requests
import shutil
import sys
import subprocess

from typing import List, Union
from time import time, sleep
from configparser import ConfigParser
from zipfile import ZipFile
from io import BytesIO

settings_file_name = './settings.ini'
control_filename = './control'

def set_action(action: str) -> None:
    with open(control_filename, 'w') as file:
        file.write(action)

def get_action() -> str:
    with open(control_filename) as file:
        return file.read()

def get_key(accepted_keys: List[str], timeout: float = 0.5) -> Union[str, None]:
    if timeout == 0:
        while (key := msvcrt.getwch().lower()) not in accepted_keys:
            pass
        return key
    start = time()
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch().lower()
            if key in accepted_keys:
                break
        elif (time() - start) > 5:
            key = None
            break
    return key

def init() -> None:
    print('Initializing')
    print('[P] Pause Bot [S] Stop Bot')
    while (key := get_key(['p', 's'])) is None:
        if get_action() != 'init':
            return
    if key == 'p':
        set_action('pause')
    elif key == 's':
        set_action('stop')
    else:
        raise Exception(f'Unknown key [running] {key}')
    
def running() -> None:
    print('Running')
    print('[P] Pause Bot [S] Stop Bot')
    while (key := get_key(['p', 's'])) is None:
        if get_action() != 'running':
            return
    if key == 'p':
        set_action('pause')
    elif key == 's':
        set_action('stop')
    else:
        raise Exception(f'Unknown key [running] {key}')
        
def pause() -> None:
    print('Pause')
    print('[R] Resume Bot [S] Stop Bot')
    while (key := get_key(['r', 's'])) is None:
        if get_action() != 'pause':
            return
    if key == 'r':
        set_action('running')
    elif key == 's':
        set_action('stop')
    else:
        raise Exception(f'Unknown key [paused] {key}')
    
def paused() -> None:
    print('Paused')
    print('[R] Resume Bot [S] Stop Bot')
    while (key := get_key(['r', 's'])) is None:
        if get_action() != 'paused':
            return
    if key == 'r':
        set_action('running')
    elif key == 's':
        set_action('stop')
    else:
        raise Exception(f'Unknown key [paused] {key}')

def stop() -> None:
    print('Waiting for stop')
    while get_action() != 'stopped':
        sleep(1)
    print('Stopped')
    os.remove(control_filename)

def get_current_version() -> str:
    if not os.path.exists('current_version'):
        with open('current_version', 'w') as file:
            file.write('0.0.0')
        return('0.0.0')
    with open('current_version') as file:
        return file.read()

def set_current_version(version: str) -> None:
    with open('current_version', 'w') as file:
        file.write(version)

def get_last_version(api_key, api_password) -> str:
    query_data = {
        'api[method]': 'get_bot_versions',
        'api[version]': '1',
        'api_key': api_key,
        'password': api_password,
    }
    query_string = urllib.parse.urlencode(query_data)
    
    get_bot_versions_url = f'http://bvb.strike.ws/bot/index.php?{query_string}'
    response = requests.get(get_bot_versions_url).json()
    
    if 'versions' in response and 'last' in response['versions'] and 'version' in response['versions']['last']:
        last_version = response['versions']['last']['version']
        return last_version
    else:
        raise Exception('No last version in response')

def download_version(version: str) -> None:
    get_bot_url = f'http://bvb.strike.ws/bot/soft/bot_versions/{version}.zip'
    bor_response = requests.get(get_bot_url)
    zip_file = ZipFile(BytesIO(bor_response.content))
    path = f'./versions/{version}'
    if os.path.exists(path):
        print(f'Path {path} already exists. Overwriting')
        shutil.rmtree(path)
    zip_file.extractall(path)
    print(f'Version {version} downloaded and unpacked')

def main() -> None:
    settings = ConfigParser()
    settings.read(settings_file_name)
    
    api_key = settings['Settings']['api_key']
    api_password = settings['Settings']['api_password']
    bot_path = settings['Settings']['bot_path'] if 'bot_path' in settings['Settings'] else None
    
    
    current_version = get_current_version()
    print(f'Current Version: {current_version}')
    
    last_version = get_last_version(api_key, api_password)
    print(f'Last Version: {last_version}')
    
    print('[R] Run Bot [U] Update Bot [Q] Quit')
    key = get_key(['r', 'u', 'q'], 0)
    if key == 'u':
        download_version(last_version)
        set_current_version(last_version)
        current_version = get_current_version()
        print('Press any key to continue')
        msvcrt.getch()
    elif key == 'q':
        return
    elif key == 'r':
        pass
    else:
        print(f'Unknown key [init] {key}')
        return
    
    # TODO: check control file and suggest continue or delete
    
    write_pyc = len(sys.argv) > 1 and sys.argv[1] == '-B'
    python_venv_path = './venv/python3.8/Scripts/python.exe'
    python_path = python_venv_path if os.path.exists(python_venv_path) else 'python.exe'
    if bot_path is None:
        bot_path = f'./versions/{current_version}/main.py'
    arguments = [python_path, '-B', bot_path] if write_pyc else [python_path, bot_path]

    if not os.path.exists(control_filename):
        set_action('init')
        subprocess.Popen(arguments, creationflags=subprocess.CREATE_NEW_CONSOLE)
    while True:
        current_action = get_action()
        if current_action == 'init':
            init()
        elif current_action == 'running':
            running()
        elif current_action == 'pause':
            pause()
        elif current_action == 'paused':
            paused()
        elif current_action == 'stop':
            stop()
            return
        elif current_action == 'stopped':
            print('Bot stopped')
            return
        else:
            raise Exception(f'Unknown action {current_action}')

if __name__ == '__main__':
    main()