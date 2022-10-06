# My Common Types and Methods Library

import os
from enum import Enum

# consts:

PLEASE_REPEAT = 'Пожалуйста попробуйте снова.'
ERROR_NOT_INT = 'Некорректный ввод: Требуется целое число. ' + PLEASE_REPEAT
ERROR_NOT_FLOAT = 'Некорректный ввод: Требуется вещественное число. ' + PLEASE_REPEAT


class escape_codes:
    CLEAR = '\033[1;1H\033[2J'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'      # курсив, может не работать, в ubuntu ok
    UNDERLINE = '\033[4m'

    FG_BLACK = '\033[30m'
    FG_RED = '\033[31m'
    FG_GREEN = '\033[32m'
    FG_YELLOW = '\033[33m'
    FG_BLUE = '\033[34m'
    FG_MAGENTA = '\033[35m'
    FG_CYAN = '\033[36m'
    FG_WHITE = '\033[37m'
    FG_GRAY = '\033[90m'
    FG_BRIGHT_RED = '\033[91m'
    FG_BRIGHT_GREEN = '\033[92m'
    FG_BRIGHT_YELLOW = '\033[93m'
    FG_BRIGHT_BLUE = '\033[94m'
    FG_BRIGHT_MAGENTA = '\033[95m'
    FG_BRIGHT_CYAN = '\033[96m'
    FG_BRIGHT_WHITE = '\033[97m'

    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_GRAY = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

    BG_DARK_PURPLE = '\033[48;5;90m'


class ForeColor(Enum):
    BLACK = escape_codes.FG_BLACK
    RED = escape_codes.FG_RED
    GREEN = escape_codes.FG_GREEN
    YELLOW = escape_codes.FG_YELLOW
    BLUE = escape_codes.FG_BLUE
    MAGENTA = escape_codes.FG_MAGENTA
    CYAN = escape_codes.FG_CYAN
    WHITE = escape_codes.FG_WHITE
    GRAY = escape_codes.FG_GRAY
    BRIGHT_RED = escape_codes.FG_BRIGHT_RED
    BRIGHT_GREEN = escape_codes.FG_BRIGHT_GREEN
    BRIGHT_YELLOW = escape_codes.FG_BRIGHT_YELLOW
    BRIGHT_BLUE = escape_codes.FG_BRIGHT_BLUE
    BRIGHT_MAGENTA = escape_codes.FG_BRIGHT_MAGENTA
    BRIGHT_CYAN = escape_codes.FG_BRIGHT_CYAN
    BRIGHT_WHITE = escape_codes.FG_BRIGHT_WHITE


class BackColor(Enum):
    BLACK = escape_codes.BG_BLACK
    RED = escape_codes.BG_RED
    GREEN = escape_codes.BG_GREEN
    YELLOW = escape_codes.BG_YELLOW
    BLUE = escape_codes.BG_BLUE
    MAGENTA = escape_codes.BG_MAGENTA
    CYAN = escape_codes.BG_CYAN
    WHITE = escape_codes.BG_WHITE
    GRAY = escape_codes.BG_GRAY
    BRIGHT_RED = escape_codes.BG_BRIGHT_RED
    BRIGHT_GREEN = escape_codes.BG_BRIGHT_GREEN
    BRIGHT_YELLOW = escape_codes.BG_BRIGHT_YELLOW
    BRIGHT_BLUE = escape_codes.BG_BRIGHT_BLUE
    BRIGHT_MAGENTA = escape_codes.BG_BRIGHT_MAGENTA
    BRIGHT_CYAN = escape_codes.BG_BRIGHT_CYAN
    BRIGHT_WHITE = escape_codes.BG_BRIGHT_WHITE
    DARK_PURPLE = escape_codes.BG_DARK_PURPLE


# methods:

def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_for_repeat():
    answer = input('Желаете повторить (Y/n)? ')
    return len(answer) == 0 or answer[0].lower() == 'y'


def console_format(text, bold=False, italic=False, underline=False, fore_color: ForeColor = None, back_color: BackColor = None):
    prefix = ''
    if (bold):
        prefix = escape_codes.BOLD
    if (italic):
        prefix += escape_codes.ITALIC
    if (underline):
        prefix += escape_codes.UNDERLINE
    if (fore_color is not None):
        prefix += fore_color.value
    if (back_color is not None):
        prefix += back_color.value
    return prefix + str(text) + escape_codes.RESET


def print_title(title):
    lines = title.split(sep='\n')
    longest_line = max(lines, key=len)
    border = len(longest_line) * '\u2550'
    print(console_format(f'{border}\n{title}\n{border}',
          bold=True, fore_color=ForeColor.BRIGHT_CYAN))
    # print(f'{escape_codes.BRIGHT_CYAN}{escape_codes.BOLD}{border}\n{title}\n{border}{escape_codes.RESET}')


def print_error(message):
    print(console_format(f'\u2757 {message}', fore_color=ForeColor.RED))
    #print(f'{escape_codes.RED}\u2757 {message}{escape_codes.RESET}')


def get_user_input_int(prompt: str, warn_out_of_range: str, func_check_if_valid) -> int:
    not_a_number = False
    out_of_range = False
    while True:
        if not_a_number:
            not_a_number = False
            print_error(ERROR_NOT_INT)
        if out_of_range:
            out_of_range = False
            print_error(warn_out_of_range)

        try:
            num = int(input(prompt))
            out_of_range = not func_check_if_valid(num)
            if not out_of_range:
                return num
        except:
            not_a_number = True


def is_out_of_range(value, min_allowed, max_allowed):
    return ((min_allowed is not None) and value < min_allowed) or ((max_allowed is not None) and value > max_allowed)


def get_user_input_int_range(prompt: str, min_allowed: int = None, max_allowed: int = None) -> int:
    not_a_number = False
    out_of_range = False
    while True:
        if not_a_number:
            not_a_number = False
            print_error(ERROR_NOT_INT)
        if out_of_range:
            out_of_range = False
            error_out_of_range = ''
            if (min_allowed is not None) and (max_allowed is not None):
                error_out_of_range = f'Число должно быть в интервале от {min_allowed} до {max_allowed}! {PLEASE_REPEAT}'
            elif min_allowed is not None:
                error_out_of_range = f'Число не должно быть меньше {min_allowed}! {PLEASE_REPEAT}'
            else:
                error_out_of_range = f'Число не должно быть больше {max_allowed}! {PLEASE_REPEAT}'
            print_error(error_out_of_range)

        try:
            num = int(input(prompt))
            out_of_range = is_out_of_range(num, min_allowed, max_allowed)
            if not out_of_range:
                return num
        except:
            not_a_number = True


def make_decimal_separator_invariant(expected_float_str: str) -> str:
    expected_float_str = expected_float_str.replace(',', '.')
    num_of_extra_dots = expected_float_str.count('.') - 1
    if num_of_extra_dots > 0:
        expected_float_str = expected_float_str.replace(
            '.', '', num_of_extra_dots)
    return expected_float_str


def get_user_input_float(prompt: str, warn_out_of_range: str, func_check_if_valid):
    not_a_number = False
    out_of_range = False
    while True:
        if not_a_number:
            not_a_number = False
            print_error(ERROR_NOT_FLOAT)
        if out_of_range:
            out_of_range = False
            print_error(warn_out_of_range)

        try:
            inp = input(prompt)
            inp = make_decimal_separator_invariant(inp)
            num = float(inp)
            out_of_range = not func_check_if_valid(num)
            if not out_of_range:
                return num
        except:
            not_a_number = True
