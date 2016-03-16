__author__ = 'a.jha'

import math

TWO_MILLION = 2000000


def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for current in range(3, int(math.sqrt(number) + 1), 2):
            if number % current == 0:
                return False
        return True
    return False


def get_prime():
    current = 2
    while True:
        if is_prime(current):
            yield current
        current += 1


if __name__ == '__main__':
    _sum = 0
    for prime in get_prime():
        if prime >= TWO_MILLION:
            break
        _sum += prime
    print _sum