# Задана натуральная степень k. Сформировать случайным образом список коэффициентов (значения от 0 до 100)
# многочлена и записать в файл многочлен степени k
# k - максимальная степень многочлена, следующий степень следующего на 1 меньше и так до ноля
# Коэффициенты расставляет random, поэтому при коэффициенте 0 просто пропускаем данную итерацию степени

# Пример:
# k=2 -> 2x² + 4x + 5 = 0 или x² + 5 = 0 или 10x² = 0
# k=5 -> 3x⁵ + 5x⁴ - 6x³ - 3x = 0

from unittest import result
import common
from os.path import join as combine_path
from conversions import to_superscripted_number
from iofunctions import get_files_paths
import random

# constants:

FILES_DIR = 'files'
OUTPUT_FILENAME = 'generated_polynomial.txt'

WARN_OUT_OF_RANGE = 'Некорректный ввод: Допускается только целое положительное число! ' \
    + common.PLEASE_REPEAT

MIN_COEFFICIENT = 0
MAX_COEFFICIENT = 100

MULT_SIGN = '\u22c5'


# methods:
def to_term_str(degree, coefficient, variable_name):
    if coefficient == 0:
        return None
    if degree == 0:
        return str(coefficient)

    degree_str = to_superscripted_number(degree) if degree > 1 else ''

    if coefficient == 1:
        return variable_name + degree_str
    
    return f'{coefficient}{MULT_SIGN}{variable_name}{degree_str}'


def generate_polynomial_string(degree, minimum, maximum, variable_name):
    if degree == 0:
        return '0 = 0'

    if minimum > maximum:
        minimum, maximum = maximum, minimum
    poly_dict: dict[int, int] = None
    # формируем словарь абс значений коэффициентов при членах со степенями от 1,
    # но так, чтобы их сумма была отлична от нуля, иначе сформируется некорректное ложное равенство
    while poly_dict is None or sum(poly_dict.values()) == 0:
        poly_dict = {c: random.randint(minimum, maximum)
                     for c in range(1, degree+1)}
    poly_dict[0] = random.randint(minimum, maximum)

    poly_terms = [to_term_str(k, value, variable_name)
                  for k, value in sorted(poly_dict.items(), reverse=True) if value != 0]

    result: str = ' @ '.join(poly_terms)
    while result.find('@') >= 0:
        result = result.replace('@', random.choice(['+', '-']), 1)

    if random.choice(['+', '-']) == '-':
        result = '-' + result

    return result + ' = 0'


def get_variable_name_from_user():
    wrong_input = False
    while True:
        if wrong_input:
            common.print_error(
                'Некорректный воод: Требуется одна буква латинского алфавита! '+common.PLEASE_REPEAT)

        inp_str = input(
            'Введите имя переменной (одна буква латинского алфавита): ')
        if len(inp_str) == 1 and inp_str.isalpha():
            return inp_str
        wrong_input = True


def write_result_with_diagnostics_output(file_path, data_to_write):
    try:
        with open(file_path, 'w') as file:
            file.write(data_to_write)
        print(common.console_format(f'Результат успешно записан в файл {file_path}',
                                    fore_color=common.ForeColor.BRIGHT_GREEN))
    except OSError:
        common.print_error(
            f'Не удалось открыть файл {file_path} для записи результата.')
    print()


# main flow:
user_answer = True

while(user_answer):
    common.console_clear()
    common.print_title(
        'Формирование случайным образом многочлена с одной переменной,'
        '\nу которого абсолютные значения коэффициентов лежат в диапазоне от 0 до 100.')

    variable_name = get_variable_name_from_user()

    k = common.get_user_input_int(
        'Задайте степень многочлена (натуральное число): ', WARN_OUT_OF_RANGE, lambda a: a > 0)

    generated_polynomial = generate_polynomial_string(
        k, MIN_COEFFICIENT, MAX_COEFFICIENT, variable_name)

    print(common.console_format('\nСгенерированный многочлен:\n', bold=True))

    print(common.console_format(generated_polynomial,
          fore_color=common.ForeColor.BRIGHT_YELLOW))

    print()
    write_result_with_diagnostics_output(
        combine_path(FILES_DIR, OUTPUT_FILENAME),
        generated_polynomial
    )

    user_answer = common.ask_for_repeat()
