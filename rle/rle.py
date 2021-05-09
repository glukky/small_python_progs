#!/usr/bin/env python3

#import sys

_DIGITS = [str(x) for x in range(0, 10)]


class InvalidInput(Exception):
    pass

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


def rle(input_str):
    symbol = None
    count = 1
    output_str = ''
    # print(input_str)
    for next_symbol in input_str:
        if ord(next_symbol) < ord('A') or ord(next_symbol) > ord('Z'):
            raise InvalidInput('Input must match [A-Z]+ regexp. ')
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

def unrle(input_str):
    """
    A4B5C16AVCA3 -> AAAABBBBB(C*16)AVCAAA
    """
    result_str = ''
    presymbol = ''
    count = 0
    for symbol in input_str:
        if ord(symbol) >= ord('A') and ord(symbol) <= ord('Z'):
            result_str += presymbol * (count if count else 1)
            presymbol = symbol
            count = 0
        elif ord(symbol) >= ord('0') and ord(symbol) <= ord('9'):
            count = count * 10 + (ord(symbol) - ord('0'))
        else:
            raise InvalidInput('Input must match ([A-Z][0-9]*)*')
    result_str += presymbol * (count if count else 1)
    return result_str


def test_rle(input_str, output_str, expect_exception=False):
    conv_input = None
    try:
        conv_input = rle(input_str)
        unpacked = unrle(conv_input)
    except InvalidInput as e:
        if expect_exception:
            return

    assert conv_input == output_str, 'Test `{}` != `{}` failed'.format(conv_input, output_str)
    assert input_str == unpacked, 'Test `{}` != `{}` failed'.format(input_str, unpacked)


def test_all_rle():
    test_rle('', '')
    test_rle('AAAABBBCCCCC', 'A4B3C5')
    test_rle('AAAABBBCCCCC 10', '', expect_exception=True)
    test_rle('AAAABBB', 'A4B3')
    test_rle('AAAA', 'A4')
    test_rle('A' * 16, 'A16')
    test_rle('ABC', 'ABC')
    print('All tests are OK')


def main():
    test_all_rle()


if __name__ == '__main__':
    main()
