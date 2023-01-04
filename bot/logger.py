import math
import os
import os.path

from datetime import datetime


current_log = ''
in_middle = False
header_char = '='

def time_prefix(datetime: datetime) -> str:
    ms = datetime.microsecond // 1000
    return f'[{datetime.strftime("%H:%M:%S")}.{ms:03}]: '

header_width = 80 - len(time_prefix(datetime.now()))

def log(message: str, end_line: bool = True) -> None:
    global current_log
    global in_middle

    if not in_middle:
        out_message = f'{time_prefix(datetime.now())}{message}'
    else:
        out_message = message
    current_log += out_message
    in_middle = not end_line
    if end_line:
        current_log += '\n'
        print(out_message)
    else:
        print(out_message, end='', flush=True)

def header(header: str) -> None:
    global current_log
    global in_middle
    global header_width
    global header_char

    if in_middle:
        current_log += '\n'
        print('')
    in_middle = False
    log('')
    log(header_width * header_char)
    
    header_len = len(header)
    side_char_count = (header_width - header_len - 2) / 2
    log(f'{math.ceil(side_char_count) * "="} {header} {math.floor(side_char_count) * "="}')
    
    log(header_width * header_char)
    log('')

def line() -> None:
    global current_log
    global in_middle
    global header_width
    global header_char

    if in_middle:
        current_log += '\n'
        print('')
    in_middle = False
    log('')
    log(header_width * header_char)
    log('')

def write_log(bet_try: int) -> None:
    global current_log

    now = datetime.now()
    log_path = now.strftime(f'./logs/%Y-%m-%d/%H-%M-%S-{bet_try}.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_file.write(current_log)
        current_log = ''
