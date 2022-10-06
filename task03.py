# Задайте последовательность цифр. Напишите программу, которая выведет список
# неповторяющихся элементов исходной последовательности.

import string
import common


# methods:

def get_individuals(digits_list):
    return [n for n in set(digits_list) if digits_list.count(n) == 1]


def get_numeric_series_from_user():
    wrong_input = False

    while True:
        if wrong_input:
            common.print_error(
                'Некорректный ввод: Допускается только последовательность цифр! ' + common.PLEASE_REPEAT)

        inp_str = input('Введите последовательность цифр: ')
        # удаляем всякую пунктуацию:
        inp_str = inp_str.translate(str.maketrans('', '', string.punctuation))
        # удаляем все пробельные символы:
        inp_str = ''.join(inp_str.split())
        if inp_str.isdigit():
            return (inp_str, list(map(int, inp_str)))
        wrong_input = True


# main flow:

user_answer = True

while(user_answer):
    common.console_clear()
    common.print_title(
        'Формирование списка неповторяющихся элементов исходной последовательности цифр')

    input_str, digits_series = get_numeric_series_from_user()
    individuals = get_individuals(digits_series)

    if len(individuals) == 0:
        print(common.console_format(f'\nПоследовательность "{input_str}" не содержит неповторяющихся цифр.',
              fore_color=common.ForeColor.BRIGHT_YELLOW))
    else:
        print(input_str, '->',
              common.console_format(individuals, fore_color=common.ForeColor.BRIGHT_YELLOW))

    print()

    user_answer = common.ask_for_repeat()
