#!/usr/bin/env python3

import sys

_DIGITS = [str(x) for x in range(0, 10)]


def mystr(symbol, count):
    if symbol is None:
        return ''
    if count == 1:
        return symbol
    list_num = []
    while count > 0:
        number = count % 10
        count = count // 10
        list_num.append(_DIGITS[number])
    return symbol + ''.join(list_num[::-1]) 


def main():
    with open(sys.argv[1], 'r') as f:
        with open(sys.argv[2], 'w') as f_out:
            next_symbol = f.read(1)
            symbol = None
            count = 1
            while next_symbol:
                if symbol == next_symbol:
                    count += 1
                else:
                    f_out.write(mystr(symbol, count))
                    count = 1
                    symbol = next_symbol
                next_symbol = f.read(1)


if __name__ == '__main__':
    main()
