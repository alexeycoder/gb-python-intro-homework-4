# Задайте натуральное число N. Напишите программу, которая составит список простых множителей числа N.

import common


# consts:

WARN_OUT_OF_RANGE = 'Требуется целое положительное число, большее 1. ' + \
    common.PLEASE_REPEAT


# types:

class Primes:
    """ Генератор простых чисел с кэшированием для оптимизации
    повторного вызова.
    """
    __found_primes = [2, 3, 5, 7]

    @staticmethod
    def generator(maximum):
        for prime in Primes.__found_primes:
            if prime <= maximum:
                yield prime

        testing_number = Primes.__found_primes[-1] + 2
        while testing_number <= maximum:

            if testing_number % 10 == 5:
                testing_number += 2
                continue

            test_limit = int(testing_number**0.5) + 1
            for prime in Primes.__found_primes:
                if prime > test_limit:
                    Primes.__found_primes.append(testing_number)
                    yield testing_number
                    break
                if testing_number % prime == 0:
                    break
            else:
                Primes.__found_primes.append(testing_number)
                yield testing_number
            testing_number += 2


# methods:

def get_prime_multipliers(number):
    return [d for d in Primes.generator(number) if number % d == 0]


def factorize(number, prime_multipliers_list):
    factorization_list = []
    for multiplier in sorted(prime_multipliers_list, reverse=True):
        while number % multiplier == 0:
            factorization_list.append(multiplier)
            number //= multiplier
    return factorization_list[::-1]


# main flow:

user_answer = True

while(user_answer):
    common.console_clear()
    common.print_title(
        'Формирование списка простых множителей заданного натурального числа')

    num = common.get_user_input_int(
        'Введите натуральное число, большее 1: ', WARN_OUT_OF_RANGE, lambda a: a > 1)

    prime_multipliers = get_prime_multipliers(num)

    if len(prime_multipliers) == 1:
        print(common.console_format(
            f'\nЧисло {num} является простым и не имеет иных множителей'
              ' кроме единицы и самого себя.\n',
              fore_color=common.ForeColor.BRIGHT_YELLOW))
    else:
        factorization = factorize(num, prime_multipliers)
        print()
        print(num, '->', common.console_format(prime_multipliers,
                                               bold=True,
                                               fore_color=common.ForeColor.BRIGHT_YELLOW))
        print(f'\nФакторизация числа {num}:\n')
        print(num, '=',
              common.console_format(' \u00d7 '.join(map(str, factorization)),
                                    fore_color=common.ForeColor.BRIGHT_YELLOW))
        print()

    user_answer = common.ask_for_repeat()
