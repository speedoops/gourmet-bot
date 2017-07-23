#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import glob
import re
import string

with open('history.txt', encoding='utf-8') as fin:
    for line in fin: 
        line = re.sub(r'^[^：]*：(.*?)；(.*?)，(\d{11})。.*$', r'\g<1>=\g<2>=\g<3>', line)
        #line = re.sub('^(.*)$', '\g<1>=', line)
        print(line)
