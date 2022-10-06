# Вычислить число пи c заданной точностью *d*

import common
import math
import datetime


# consts:

PRECISION_LIMIT = 1E-10
WARN_OUT_OF_RANGE = f'Число должно быть не больше 1 и не меньше {PRECISION_LIMIT}. ' + \
    common.PLEASE_REPEAT


# methods:

def calc_pi_leibniz(precision):
    #precision = 10 ** (-(precision_digits + 1))
    precision /= 10
    d = 3
    sign = -1
    s = 4
    abs_addition = 1
    while abs_addition > precision:
        abs_addition = 4 / d
        s += sign*abs_addition
        sign = -sign
        d += 2
    return s


def calc_pi_bailey_borwein_plouffe(num_of_decimals):
    def formula(n):
        eight_n = n*8
        sixteen_pow_n = 16**n
        return (4/(eight_n + 1) - 2/(eight_n + 4) - 1/(eight_n + 5) - 1/(eight_n + 6))/sixteen_pow_n

    return sum([formula(i) for i in range(num_of_decimals+1)])


def truncate(real_num, num_of_decimals):
    magnitude = 10 ** num_of_decimals
    real_num = math.trunc(real_num * magnitude)
    return real_num / magnitude


def num_of_decimals(real_num: float):
    if real_num == 0:
        return 100
    if real_num >= 1:
        return 0

    return int(math.ceil(math.log10(1/real_num)))


# main flow:
user_answer = True

while(user_answer):
    common.console_clear()
    common.print_title(
        'Вычисление числа \u03c0 c заданной точностью'
        '\nТочность задаётся в виде вещественного числа вида 0.001')

    d = common.get_user_input_float('Введите вещественное число, обозначающее минимальную точность: ',
                                    WARN_OUT_OF_RANGE, lambda a: a <= 1 and a >= PRECISION_LIMIT)

    decimal_places = num_of_decimals(d)
    print('\nРеференсное значение:\n')
    print('\u03c0 =', truncate(math.pi, decimal_places))

    print('\nРезультат вычисления с использованием ряда Лейбница:\n')

    start_time = datetime.datetime.now()
    pi = calc_pi_leibniz(d)
    elapsed_time = datetime.datetime.now() - start_time
    pi_truncated = truncate(pi, decimal_places)

    print('\u03c0 =', pi_truncated)
    print(f'\n(затрачено времени: {elapsed_time.total_seconds()} сек)')

    print('\nРезультат вычисления с использованием формула Бэйли—Боруэйна—Плаффа:\n')

    start_time = datetime.datetime.now()
    pi_2 = calc_pi_bailey_borwein_plouffe(decimal_places)
    elapsed_time = datetime.datetime.now() - start_time
    pi_2_truncated = truncate(pi_2, decimal_places)

    print('\u03c0 =', pi_2_truncated)
    print(f'\n(затрачено времени: {elapsed_time.total_seconds()} сек)')
    print()

    user_answer = common.ask_for_repeat()
