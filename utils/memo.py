#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.config
import re

MEMO_FILE = 'history.txt'

# 初始化日志
LOG = logging.getLogger(__name__)

def appendMemo(msg, text):
    LOG.debug('appendMemo: ')
    try:
        text = re.sub(r' (\d{1,2}[、|.])', '\n\1', msg.text)
        f = open(MEMO_FILE, 'a')
        f.write('--- %s %s ---\n' % (msg.receive_time, msg.sender))
        f.write(text)
        f.write('\n')
        f.close()
        return '搞定！saved in %s.' % MEMO_FILE
    except Exception as e:
        return 'Exception: %s' % e

def getOneAddress(word):
    list = []
    with open(MEMO_FILE, encoding='utf-8') as fin:
        for line in fin:
            match = re.match(r'^[^：]*：(?P<address>.+?)；(?P<name>.+?)，(?P<phone>\d{11})。.*$', line)
            if match:
                line = '%s；%s，%s' % (match.group('address'), match.group('name'), match.group('phone'))
                if re.match(r'.*%s.*' % word, line):
                    return line

def replace_with_addresses(input):
    isPattern = False
    pattern = ''
    output = ''

    for ch in input:
        if ch == '{':
            isPattern = True
            continue
        elif ch == '}':
            output += '[%s]' % getOneAddress(pattern)
            isPattern = False
            pattern = ''
            continue

        if isPattern:
            pattern += ch
        else:
            output += ch

    return output


if __name__ == "__main__":
    input = '中文，hello,{谢津},dldlflf{刘丽} dkkrkzhon'
    output = replace_with_addresses(input)
    print(output+'\n')
