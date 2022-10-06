import common
from os.path import join as combine_path
from conversions import to_superscripted_number
from iofunctions import get_files_paths

# constants:

FILES_DIR = 'files'
FILES_COMMON_NAME = 'source_polynomial'
FILES_EXT = '.txt'
OUTPUT_FILENAME = 'result_polynomial.txt'
VARIABLE_NAME = 'x'

# uncomment for another version:
# V_PREFIX = 'v2_'
# FILES_COMMON_NAME = V_PREFIX + FILES_COMMON_NAME
# OUTPUT_FILENAME = V_PREFIX + OUTPUT_FILENAME


# methods:

def summarize_dictionaries(*dictionaries: dict[int:float]):
    result: dict[int, float] = {}
    for dictionary in dictionaries:
        result = {key: result.get(key, 0) + dictionary.get(key, 0)
                  for key in set(result) | set(dictionary)}
    return result

# def summarize_dictionaries(dictionary_a: dict, dictionary_b: dict):
#     return {key: dictionary_a.get(key, 0) + dictionary_b.get(key, 0) for key in set(dictionary_a) | set(dictionary_b)}


def remove_consequent_duplicates(string: str, character: str):
    character_twice = str(character)*2
    length = -1
    while len(string) != length:
        length = len(string)
        string = string.replace(character_twice, character)
    return string


def expand_brackets(string: str):
    string = string.replace(')', '') \
        .replace('-(-', '+') \
        .replace('+(+', '+') \
        .replace('-(+', '-') \
        .replace('+(-', '-') \
        .replace('(', '')
    return string


def normalize_input(input_line: str):
    """
    Приводит вольготное строковое представление к единообразному для дальнеёшего парсинга.
    """
    normalized_line = input_line.strip().lower()
    # ''.join(s.split()) - удаляет все пробельные символы:
    normalized_line = ''.join(normalized_line.split())
    # -- даёт +, но надо идти в обратном порядке, пока не было удаления дубликатов:
    normalized_line = normalized_line[::-1].replace('--', '+')[::-1]
    # теперь можно удалить дублирования:
    normalized_line = remove_consequent_duplicates(normalized_line, '+')
    normalized_line = remove_consequent_duplicates(normalized_line, '-')
    normalized_line = remove_consequent_duplicates(normalized_line, '=')
    normalized_line = normalized_line.replace('+-', '-').replace('-+', '-')
    # раскрываем скобки вокруг членов уравнения:
    normalized_line = expand_brackets(normalized_line)

    # в общем случае может присутствовать правая часть уравнения - переносим влево:
    left_right_parts = normalized_line.split('=')
    normalized_line = left_right_parts[0]
    if len(left_right_parts) > 1:
        right_part = left_right_parts[1].strip()
        if not right_part in ['0', '+0', '-0']:
            right_part = right_part.replace('+', '~') \
                .replace('-', '+') \
                .replace('~', '-')
            if not right_part.startswith('+') and not right_part.startswith('-'):
                right_part = '-' + right_part
            normalized_line += right_part

    normalized_line = normalized_line.replace('+', ' +').replace('-', ' -')
    normalized_line = normalized_line.replace(',', '.')
    return normalized_line


def get_term_from_raw(raw_term):
    """
    Преобразует строковое представление члена многочлена в кортеж вида(степень: int, коэффициент: float)

    'term' - член многочлена
    """
    coefficient = 0
    degree = 0

    if raw_term.find('^') < 0:  # свободный член - степень 0
        coefficient = float(raw_term)
    else:
        (coefficient_str, degree_str) = raw_term.split('^')
        # не указанные явно коэффициент и/или степень члена принимаем равными 1
        if coefficient_str in ['', '+', '-']:
            coefficient_str += '1'
        if degree_str in ['', '+', '-']:
            degree_str += '1'

        coefficient = float(coefficient_str)
        degree = int(degree_str) if degree_str != '' else 1

    return (degree, coefficient)


def get_polynomial_dict(input_line: str, variable_name: str):
    PAIR_DIV_SYMBOL = '^'
    normalized_line = normalize_input(input_line)

    # заменяем *x на просто х
    # затем заменяем x** и x^ на одиночный разделитель '^',
    # а если после всех замен остался просто x то заменяем его на '^1'
    normalized_line = normalized_line.replace(f'*{variable_name}', str(variable_name)) \
        .replace(f'{variable_name}^', PAIR_DIV_SYMBOL) \
        .replace(f'{variable_name}**', PAIR_DIV_SYMBOL) \
        .replace(variable_name, PAIR_DIV_SYMBOL+'1')

    # складируем строковые представления членов, заданных некорректно
    erroneous_raw_terms = []
    # скаладируем словарь { степень : коэффициент }
    terms_dict = {}
    for raw_term in normalized_line.split():
        try:
            (degree, coefficient) = get_term_from_raw(raw_term)

            existing_coef = terms_dict.get(degree)
            if existing_coef is not None:
                coefficient += existing_coef

            terms_dict[degree] = coefficient

        except ValueError:  # or TypeError:
            erroneous_raw_terms.append(raw_term)

    return (terms_dict, erroneous_raw_terms)


def polynomial_dict_to_human_readable(polynomial_dictionary: dict, variable_name: str, multiply_symbol: str = '\u22c5', decimals: int = None) -> str:
    """
    Преобразует словарное представление многочлена с одной переменной {степень : коэффициент}
    в удобочитаемое строковое представление
    """
    format_str = r'{:g}' if decimals is None else '{:.' + str(decimals) + '}'
    result_str_terms = []
    for degree, coefficient in sorted(polynomial_dictionary.items(), reverse=True):

        term = '-' if coefficient < 0 else '+'

        mult_symb = ''
        abs_coefficient = abs(coefficient)
        if abs_coefficient != 1:
            term += format_str.format(abs_coefficient)
            mult_symb = multiply_symbol

        if degree != 0:
            term += mult_symb + variable_name
            if abs(degree) > 1:
                term += to_superscripted_number(degree)

        result_str_terms.append(term)

    result = result_str_terms[0].replace('+', '') \
        + ''.join(result_str_terms[1:]).replace('+', ' + ').replace('-', ' - ')

    return result + ' = 0'


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = list(map(str.strip, file.readlines()))
            if len(lines) > 0:
                return ' '.join(lines)
            else:
                return None
    except OSError:
        return None


def parse_with_diagnostics_output(file_path) -> dict:
    print(common.console_format(
        f'Анализ файла {file_path}:\n', bold=True, underline=True))
    raw_data = read_file(file_path)
    if raw_data is None:
        print(common.console_format('Не удалось прочитать файл либо файл пуст.\n',
              fore_color=common.ForeColor.BRIGHT_RED))
        return {}

    pdict, erroneous_terms = get_polynomial_dict(raw_data, VARIABLE_NAME)
    print('Сырые данные: "', raw_data, '"', sep='')
    print()

    if len(pdict) > 0:
        human_readable = polynomial_dict_to_human_readable(
            pdict, VARIABLE_NAME)
        print('В канонической форме:',
              common.console_format(human_readable, fore_color=common.ForeColor.BRIGHT_YELLOW))
        print()

        if len(erroneous_terms) > 0:
            print(common.console_format(
                'Прочитано с ошибками!'
                  ' Не удалось преобразовать следующие подразумеваемые члены:',
                  fore_color=common.ForeColor.BRIGHT_MAGENTA))
            print('\t'.join(erroneous_terms))
            print()

        return pdict

    else:
        print(common.console_format('Не удалось преобразовать данные в многочлен.',
              fore_color=common.ForeColor.BRIGHT_MAGENTA))
        print()

        return {}


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

files_mask_style_name = f'{FILES_COMMON_NAME}*{FILES_EXT}'

common.console_clear()
common.print_title('Формирование многочлена с одной переменной, являющегося суммой многочленов,'
                   f'\nпрочитанных из файлов {files_mask_style_name} в дирректории {FILES_DIR}'
                   '\n(один файл \u2014 один многочлен)')

files_paths = get_files_paths(FILES_DIR, FILES_COMMON_NAME, FILES_EXT)

if files_paths is None:
    common.print_error(f'В папке {FILES_DIR} не найдено файлов '
                       f'{files_mask_style_name} с описаниями многочленов.\n')
    exit()

num_of_files = len(files_paths)
if num_of_files < 2:
    common.print_error(f'В папке {FILES_DIR} найден только один файл '
                       f'{files_mask_style_name}. Требуется хотя бы два'
                       ' файла с описаниями многочленов для суммирования.\n')
    exit()

print(common.console_format(f'В папке {FILES_DIR} найдено {num_of_files} файла(ов)'
                            f' {files_mask_style_name} с описаниями многочленов.',
                            fore_color=common.ForeColor.BRIGHT_GREEN))
print()

polynomial_dictionaries_list = []

for file_path in files_paths:
    polynomial_dictionary = parse_with_diagnostics_output(file_path)
    polynomial_dictionaries_list.append(polynomial_dictionary)

if len(polynomial_dictionaries_list) == 0:
    print(common.console_format('Нечего суммировать! :(',
          fore_color=common.ForeColor.BRIGHT_MAGENTA))
    exit()

summ_poly_dict = summarize_dictionaries(*polynomial_dictionaries_list)
summ_poly_human_readable = polynomial_dict_to_human_readable(
    summ_poly_dict, VARIABLE_NAME)

print(common.console_format(
    f'Результат суммирования многочленов:\n', bold=True, underline=True))

print(common.console_format(summ_poly_human_readable,
                            fore_color=common.ForeColor.BRIGHT_YELLOW))
print()

write_result_with_diagnostics_output(
    combine_path(FILES_DIR, OUTPUT_FILENAME),
    summ_poly_human_readable)
