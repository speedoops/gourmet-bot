#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import json
import sys
import re
import os
import logging
LOG = logging.getLogger(__name__)


def execCmd(cmd, errmsg=None):
    """ 执行系统命令，并返回命令执行结果。 """
    LOG.debug("execCmd: " + cmd)
    try:
        r = os.popen(cmd)
        text = r.read()
        r.close()
        result = "%s$ %s\n%s" % (os.getcwd(), cmd, text)
        return result
    except Exception as e:
        if errmsg:
            return errmsg
        return "Exception: %s" % e


if __name__ == "__main__":
    print(execCmd("echo abc"))

    # 'grep' 不是内部或外部命令，也不是可运行的程序或批处理文件。
    print(execCmd("grep a *.py|head -n 1"))
