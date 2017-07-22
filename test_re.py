#!/usr/bin/env python3
# coding: utf-8
import re
import logging
logger = logging.getLogger()

def ccc(text):
    import re
    match = re.match(r'!(.*?): (.*)', text)
    print('~~~')
    if match:
        print('mmmm')
        logger.debug('matched' + str(match.groups()))
        code = match.group(1)
        parm = match.group(2)
        print (code + parm)
#ccc('!#: ls')

def test1(text):
    import re
    print('-1-: %s' % text)
    #match = re.match(u'(@[^ !]* ?)?!(?P<code>.*?): (?P<text>.*)', text)
    match = re.match(r'(@[^!]*)?!(?P<code>.*?): (?P<text>.*)', text)
    if match:
        print('  matched!')
        logger.debug('matched' + str(match.groups()))
        code = match.group('code')
        text = match.group('text')
        print('  code: ' + code)
        return
    print('  not match')

def test2(text):
    import re
    print('-2-: %s' % text)
    match = re.match(r'!(.*?): (.*)', text)
    if match:
        print('  matched!')
        logger.debug('matched' + str(match.groups()))
        code = match.group(1)
        text = match.group(2)
        print('  code: ' + code)
        return
    print('  not match')

test1(' !#: ls=NotMatch')
#test2(' !#: ls')
test1('!#: ls')
test1('@a !#: ls')
test1('@刘德 !#: ls')
print('@刘德 !#: ls'.encode('utf_8'))
#test2('!#: ls')
b = b'@\xe5\x88\x98\xe5\xbe\xb7\xe2\x80\x85!#: ls'
print('s=' + b.decode("utf_8"))
s = b.decode("utf_8")
print(s.encode())
test1(b.decode("utf_8"))

cmdStr = s.replace(u'@[^! ]*', '') 
cmdStr = s.replace('!.*', '') 
cmdStr = re.sub(r'@[^! ]*', "", s)
print('cmdStr: %s' % cmdStr)