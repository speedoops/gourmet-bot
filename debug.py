#!/usr/bin/env python3
# coding: utf-8

from wxpy import *
import logging
import logging.config
import os
import re

import settings
import utils

logging.config.fileConfig("logger.conf")
logger = logging.getLogger(__name__)

# 初始化wxpy机器人对象
bot = Bot("wxpy__cache.pkl", console_qr = True)
bot.enable_puid("wxpy__puid.pkl")

def export_puid(path):
    with open(path, 'w', encoding='utf-8') as output:
        output.write("-----Friends-------\n")
        for i in bot.friends():
            output.write(i.nick_name + " ---> " + i.puid + "\n")
        
        output.write("-----Groups-------\n")
        for i in bot.groups():
            output.write(i.name + " ---> " + i.puid + "\n")
#export_puid(botname+'_puid.txt')

embed()