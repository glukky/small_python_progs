import sys

with open(sys.argv[1], 'r') as f:
    str_a = f.read(1)
    summa = 0
    number = ''
    while str_a:
        if str_a.isdigit():
            number += str_a
        else:
            if number:
                summa += int(number)
            number = ''
        str_a = f.read(1)
    print('Сумма чисел:', summa)
