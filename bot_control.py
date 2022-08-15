import os
import sys
import subprocess
import msvcrt
from time import sleep, time
from typing import List, Union

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

def main() -> None:
    if not os.path.exists(control_filename):
        print('[R] Run Bot [Q] Quit')
        key = get_key(['r', 'q'], 0)
        if key == 'r':
            set_action('init')
            python_venv_path = './venv/python3.8/Scripts/python.exe'
            python_path = python_venv_path if os.path.exists(python_venv_path) else 'python.exe'
            arguments = [python_path, '-B', './main.py'] if sys.argv[1] == '-B' else [python_path, './main.py']
            subprocess.Popen(arguments, creationflags=subprocess.CREATE_NEW_CONSOLE)
        elif key == 'q':
            return
        else:
            print(f'Unknown key [init] {key}')
            return
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