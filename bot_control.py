import os
import subprocess
import msvcrt
from time import sleep
from typing import List

control_filename = './control'

def set_action(action: str) -> None:
    with open(control_filename, 'w') as file:
        file.write(action)

def get_action() -> str:
    with open(control_filename) as file:
        return file.read()

def get_key(accepted_keys: List[str]) -> str:
    while (key := msvcrt.getwch().lower()) not in accepted_keys:
        pass
    return key

def init() -> None:
    if not os.path.exists(control_filename):
        print('[R] Run Bot [Q] Quit')
        key = get_key(['r', 'q'])
        if key == 'r':
            set_action('running')
            python_vev_path = './venv/python3.8/Scripts/python.exe'
            python_path = python_vev_path if os.path.exists(python_vev_path) else 'python.exe'
            subprocess.Popen([python_path, './main.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
            running()
            return
        elif key == 'q':
            return
        else:
            print(f'Unknown key [init] {key}')
            return
    else:
        current_action = get_action()
        if current_action == 'running':
            running()
        elif current_action == 'pause':
            paused()
        elif current_action == 'stop':
            stoppig()
        else:
            print(f'Unknown action {current_action}')
    
def running() -> None:
    print('Running')
    print('[P] Pause Bot [S] Stop Bot')
    key = get_key(['p', 's'])
    if key == 'p':
        set_action('pause')
        paused()
    elif key == 's':
        set_action('stop')
        stoppig()
    else:
        print(f'Unknown key [running] {key}')
        
    
def paused() -> None:
    print('Paused')
    print('[R] Resume Bot [S] Stop Bot')
    key = get_key(['r', 's'])
    if key == 'r':
        set_action('running')
        running()
    elif key == 's':
        set_action('stop')
        stoppig()
    else:
        print(f'Unknown key [paused] {key}')

def stoppig() -> None:
    print('Stopping')
    while get_action() != 'stopped':
        sleep(1)
    print('Stopped')
    os.remove(control_filename)

def main() -> None:
    init()
    return

if __name__ == '__main__':
    main()