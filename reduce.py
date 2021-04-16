#!/usr/bin/env python3
from functools import reduce


def mapper(x):
    print(x)


def check_mapper():
    my_list = [1, 2, 'qqqq']
    map(mapper, my_list)
    print('apply list')
    list(map(mapper, my_list))


check_mapper()


def mix_lists(*args):
    '''Соединяет элементы упорядоченных структур данных
    (тип элементов string) равной длины в соответствии с индексом,
    возвращает результат одной строкой'''
    res = []
    # формируем список из списков элементов одного индекса всех args
    res_prom = [list(x) for x in zip(*args)]
    # формируем общий список из подсписков (добавляем в конец res)
    x = map(res.extend, res_prom)
    print(x)
    # собираем элементы общего списка в одну строку
    res_str = reduce(lambda x, y: x + y, res)
    return res_str


str_1 = 'Hl r!'
str_2 = 'eoWl!'
str_3 = 'l,od!'


# print(mix_lists(str_1, str_2, str_3))
