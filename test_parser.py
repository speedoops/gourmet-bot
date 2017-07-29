#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging
LOG = logging.getLogger()

def cmdStr(text):
    return re.sub(r'@[^! ]* *', "", text)  # MEMO：字符串替换

def matchedStr(cmdStr):
    LOG.debug('remove at, cmdStr=%s' % cmdStr)
    # b'@\xe5\x88\x98\xe5\xbe\xb7 !#: ls'
    # b'@\xe5\x88\x98\xe5\xbe\xb7\xe2\x80\x85!#: ls'
    match = re.match(r'!(?P<code>.*?):[[:space:]]*(?P<text>.*)', cmdStr, re.DOTALL)
    # logger.debug(msg.text.encode())
    if match:
        LOG.debug('matched' + str(match.groups()))
        code = match.group('code')
        text = match.group('text')
        return (code, text)

str1 = '@刘德 !?: 1900489595'  # ('?', '1900489595')
str1 = '!?: 9890960816194'  # ('?', '\u20059890960816194')
cstr = cmdStr(str1)
print('cmdStr: %s' % cstr)
print(matchedStr(cstr))
