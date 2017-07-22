import logging
import logging.config

logging.config.fileConfig("logger.conf")
logger = logging.getLogger("example01")
logger = logging.getLogger()

logger.debug('This is debug message')
logger.info('This is info message')
logger.warning('This is warning message')

a = ['a', 'b']
if ('c' not in a):
    print('ddd')
else:
    print('ok')

def execCmd(cmd): 
    import os
    try:
        f = open('jdkkf/fkgkg\history.txt','w')
        
        r = os.popen(cmd)
        text = r.read()
        r.close()
        return text
    except Exception as e:
        print('Exception: %s' % e)
#execCmd('dkdk')


def test_reduce():
    l=['adam', 'LISA', 'barT']
    from functools import reduce
    s = reduce(lambda x,y: x+' '+y, l)
    print(s)

def test_arg():
    import sys
    botname = 'ade'
    print(len(sys.argv))
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            print(arg)
test_arg()