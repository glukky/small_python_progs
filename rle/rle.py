#!/usr/bin/env python3

#import sys

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
    # return symbol + ''.join(list_num[::-1]) 
    return symbol + ''.join(list_num) 


def rle(input_str):
    symbol = None
    count = 1
    output_str = ''
    # print(input_str)
    for next_symbol in input_str:
        if symbol == next_symbol:
            count += 1
        else:
            chunk = mystr(symbol, count)
            # print('    ', chunk)
            output_str += chunk
            count = 1
            symbol = next_symbol
    chunk = mystr(symbol, count)
    # print('    ', chunk)
    output_str += chunk
    return output_str


def test_rle(input_str, output_str):
    conv_input = rle(input_str)
    assert conv_input == output_str, 'Test `{}` != `{}` failed'.format(conv_input, output_str)


def test_all_rle():
    test_rle('', '')
    test_rle('AAAABBBCCCCC', 'A4B3C5')
    test_rle('AAAABBB', 'A4B3')
    test_rle('AAAA', 'A4')
    test_rle('ABC', 'ABC')
    print('All tests are OK')


def main():
    test_all_rle()


if __name__ == '__main__':
    main()
