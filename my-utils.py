#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import json
import sys
import re
import os
import logging
logger = logging.getLogger()

def _getComCode(code):
    url = 'http://www.kuaidi100.com/autonumber/autoComNum?text=' + code
    page = urlopen(url)
    jsonStr = page.read().decode('utf8')
    print(jsonStr)
    jsonObj = json.loads(jsonStr)
    return jsonObj.get('auto')[0].get('comCode')
    
def getExpressStatus(code):
    company = _getComCode(code)
    print('company: ' + company)
    
    url='http://www.kuaidi100.com/query?type=%s&postid=%s' % (company,code)
    page = urlopen(url)
    jsonStr = page.read().decode('utf8')
    print(jsonStr)
    jsonObj = json.loads(jsonStr)

    if (jsonObj.get('ischeck')=='1'):
        status = '已签收'
    else:
        status = '在途'

    return '%s: %s\n%s %s' % (code, status, 
        jsonObj.get('data')[0].get('time'), jsonObj.get('data')[0].get('context'))
    
def execCmd(cmd, errmsg=None): 
    logger.debug('execCmd: ' + cmd)
    try:
        r = os.popen(cmd)  
        text = r.read()  
        r.close()
        result = '$ %s\n%s' %(cmd, text)
        return result
    except Exception as e:
        if errmsg:
            return errmsg
        return 'Exception: %s' % e

# def getOneAddress(name):
#     ret = execCmd("grep '%s' history.txt" % name)
#     return ret.replace('\n', '|')

def getOneAddress(word):
    list = []
    with open('history.txt', encoding='utf-8') as fin:
        for line in fin:
            match = re.match(r'^[^：]*：(?P<address>.+?)；(?P<name>.+?)，(?P<phone>\d{11})。.*$', line)
            if match:
                line = '%s；%s，%s' % (match.group('address'), match.group('name'), match.group('phone'))
                if re.match(r'.*%s.*' % word, line):
                    return line

def getUserAddresses(input):
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
    input = '中文，hello,{code},dldlflf{bb} dkkrkzhon'
    output = getUserAddresses(input)
    print(output)

    #print(execCmd('grep a test.py|head -n 1')) 

    #print('\n' + getExpressStatus('175032217629') + '\n')

    '''
    while True:
        try:
            code = input("Input express number, or '000' to exit：")
            code = code.strip()
            if code == '':
                code = '9890929953333'
            if code == '000':
                break
            print(getExpressStatus(code))
        except Exception:
            break
    '''
    pass