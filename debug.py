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
bot = Bot(settings.WXPY_SESSION_CACHE_FILE, console_qr=settings.WXPY_CONSOLE_QR_MODE)
bot.enable_puid(settings.WXPY_PUID_CACHE_FILE)

embed()