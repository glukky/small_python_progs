#!/usr/bin/python3
# coding: utf-8


def letter(a):
    """Возвращает True, если символ является буквой,
       и False, если символ - не буква.
       Знак ' будем считать буквой."""
    if a == ' ':
        return False
    elif a == '-':
        return False
    elif a == '"':
        return False
    elif a == '.':
        return False
    elif a == ',':
        return False
    elif a == ':':
        return False
    elif a == '!':
        return False
    elif a == '?':
        return False
    elif a == ';':
        return False
    elif a == '[':
        return False
    elif a == ']':
        return False
    elif a == '(':
        return False
    elif a == ')':
        return False
    else:
        return True


def search_word(a, Z):
    """Ищет элемент "a" в списке Z. Если находит, возвращает индекс элемента,
       в ином случае возвращает -1."""
    i = -1
    for k in range(len(Z)):
        if Z[k] == a:
            i = k
            return i
    return i


def sort_AB(A, B, x):
    """Сортирует список В по убыванию. Меняет местами соответствующие
       элементы списка А. x - индекс увеличившегося на единицу элемента
       списка В."""
    while B[x] > B[x - 1] and x > 0:
        B[x], B[x - 1] = B[x - 1], B[x]
        A[x], A[x - 1] = A[x - 1], A[x]
        x -= 1


with open('11619716_utf.txt', mode='r', encoding='utf-8') as file:
                                    # открываем текстовый файл в переменную file
    i = 0                          # количество разных слов в тексте -1
    A = []                         # список из уникальных слов в тексте
    B = []                         # список кол-ва уник. слов (А[i] соотв. B[i])

    for line_base in file:             # берём строки по одной из file
        line = line_base.lower()       # преобразование больших букв в маленькие
        # print(line, len(line))
        word = ""                      # переменная для уникального слова
        while len(line) > 1:           # перебираем символы до конца строки
            # print(letter(line[0]))
            # print(line)
            while len(line) > 1 and letter(line[0]):     # проверяем, является ли символ буквой"
                word = word + line[0]    # дописываем "букву" в конец искомого слова
                line = line[1:len(line)]  # отрезаем найденную букву от нач. стр
                # print('line=', line, len(line))
            line = line[1:len(line)]  # отрезаем незначащий символ от нач. стр
            # print('line=', line, len(line))
            # print(word)
            if len(word) > 0:         # если "слово" найдено
                pos = search_word(word, A)  # сверяем "слово" со списком уник.сл.
                if pos == -1:         # если слово уникально, добавляем его
                    A.append(word)    # в конец списка А
                    B.append(1)       # в соотв. эл. списка B пишем 1
                    i += 1            # увелич. счётчик уникальных слов
                else:                 # если "слово" уже встречалось в тексте
                    B[pos] += 1       # в B увел. на 1 эл-т, соотв. эл-ту А
                    sort_AB(A, B, pos)  # сортируем В(+А соотв) по убыванию
                word = ""             # обнуляем переменную для поиска уник.сл.
    if i > 99:                        # смотрим, как много уник.слов найдено
        for k in range(100):          # выводим самые частые 100
            print(A[k], '= ', B[k])
    else:
        for k in range(i):            # или самые частые, сколько есть (<100)
            print(A[k], '= ', B[k])
