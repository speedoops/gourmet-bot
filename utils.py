# -*- coding: UTF-8 -*-
 
from urllib.request import urlopen
import json
import sys
import re
import os
import logging
logger = logging.getLogger()

def getComCode(code):
    url = 'http://www.kuaidi100.com/autonumber/autoComNum?text=' + code
    page = urlopen(url)
    jsonStr = page.read().decode('utf8')
    print(jsonStr)
    jsonObj = json.loads(jsonStr)
    return jsonObj.get('auto')[0].get('comCode')
    
def getExpressStatus(code):
    company = getComCode(code)
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
    
def execCmd(cmd): 
    logger.debug('execCmd: ' + cmd)
    try:
        r = os.popen(cmd)  
        text = r.read()  
        r.close()
        result = '$ %s\n%s' %(cmd, text)
        return result
    except Exception as e:
        return 'Exception: %s' % e

if __name__ == "__main__":  
    #print(execCmd('grep a test.py|head -n 1'))  
    print('\n' + getExpressStatus('175032217629') + '\n')
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