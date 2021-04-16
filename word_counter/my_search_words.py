#!/usr/bin/python3

import sys
import re


def main():
    word_count = {}

    with open(sys.argv[1], mode='r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().lower().split(' ')
            for word in words:
                word = re.sub(r'[.!,_–-]', '', word)
                if not word:
                    continue

                # а вообще тут надо использовать defaultdict
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1

        word_count_list = [
            # в python2 тут придётся писать iteritems
            (w, c) for w, c in word_count.items()
        ]
        # в python2 придётся писать `cmp=` вместо `key=`
        word_count_sorted = sorted(word_count_list, key=lambda x: x[1], reverse=True)

        for i in range(100):
            print(word_count_sorted[i])


if __name__ == '__main__':
    main()
