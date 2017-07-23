#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用快递网站API查询物流状态
---

http://www.kuaidi100.com/
https://www.trackingmore.com/api-python.html
"""

import urllib.request
import json
import logging
logger = logging.getLogger()


def detect_shipment_carrier(tracking_number):
    """ 根据运单号自动推测承运商代码。

    :param tracking_number: 运单号

    .. warning:: 如果一个号码对应有多个承运商，则自动选择第一个 ———— 这意味着自动推断的结果可能与实际的不一致。
    """
    try:
        urlStr = "http://www.kuaidi100.com/autonumber/autoComNum?text=" + tracking_number
        jsonStr = urllib.request.urlopen(urlStr).read().decode("utf8")
        # logger.debug(jsonStr)

        jsonObj = json.loads(jsonStr)
        carrier_code = jsonObj.get("auto")[0].get("comCode")
        #logger.debug("carrier_code for %s is: %s", tracking_number, carrier_code)
        return carrier_code
    except Exception as e:
        logger.error('detect_shipment_carrier: %s', e)
        return None


def get_shipment_status(tracking_number, carrier_code=None):
    """ 根据运单号获取快递状态。

    :param tracking_number: 运单号
    :param carrier_code: 承运商代码
    """
    try:
        if not carrier_code:
            carrier_code = detect_shipment_carrier(tracking_number)
        #logger.debug(carrier_code)

        urlStr = "http://www.kuaidi100.com/query?type=%s&postid=%s" % (
            carrier_code, tracking_number)
        jsonStr = urllib.request.urlopen(urlStr).read().decode("utf8")
        #logger.debug(jsonStr)

        jsonObj = json.loads(jsonStr)
        if (jsonObj.get("status") == "200"):
            status = "已签收" if (jsonObj.get("ischeck") == "1") else "在途"
            return "%s(%s): %s | %s %s" % (tracking_number, carrier_code, status,
                                        jsonObj.get("data")[0].get("time"), 
                                        jsonObj.get("data")[0].get("context"))
        else:
            return "%s(%s): %s" % (tracking_number, carrier_code, jsonObj.get("message"))
    except Exception as e:
        logger.error('get_shipment_status: %s', e)
        return None

def replace_with_statuses(input):
    number = ''
    output = ''

    input += ' ' # 填充一个字符简化边界处理
    for ch in input:
        if ch.isdigit():
            number += ch
        elif number != '':            
            if len(number) > 9:
                #print("=== %s; %s" % (ch, number))
                status = get_shipment_status(number)
                if status:
                    output += '[%s]' % status
                else:
                    output += '[%s]' % number
            else:
                #print("--- %s; %s" % (ch, number))
                output += number
            number = ''
            output += ch
        else:
            #print("~~~ %s; %s" % (ch, number))
            output += ch
    
    return output
 

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    print('\n' + get_shipment_status("7707890245"))
    #print('\n' + get_shipment_status("175032217629"))
    print('\n' + replace_with_statuses("70456204032818"))
    #print('\n' + replace_with_statuses("175032217629, 7707890245"))