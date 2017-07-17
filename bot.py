#!/usr/bin/env python3
# coding: utf-8

from wxpy import *
import logging
import logging.config
import os
import re
import utils

logging.config.fileConfig("logger.conf")
logger = logging.getLogger(__name__)

botname = 'wxpy_'
if len(sys.argv) > 1:
    botname += sys.argv[1]

def onLogout():
    import time
    ISOTIMEFORMAT='%Y-%m-%d %X' # http://blog.csdn.net/caisini_vc/article/details/5619954
    logger.warn('---\nlogged out on %s\n---' % time.strftime(ISOTIMEFORMAT, time.localtime()))
    os._exit(0)

# 初始化wxpy机器人对象
bot = Bot(botname+'_cache.pkl', console_qr=True, logout_callback=onLogout)
bot.enable_puid(botname+'_puid.pkl')

def export_puid(path):
    with open(path, 'w', encoding='UTF-8') as output:
        output.write("-----Friends-------\n")
        for i in bot.friends():
            output.write(i.nick_name + " ---> " + i.puid + "\n")
        
        output.write("-----Groups-------\n")
        for i in bot.groups():
            output.write(i.name + " ---> " + i.puid + "\n")
#export_puid(botname+'_puid.txt')

def appendMemo(msg, text):
    logger.debug('appendMemo: ')
    try:
        text = re.sub(r' (\d{1,2}[、|.])', '\n\1', msg.text)
        f = open('history.txt','a')
        f.write('--- %s %s ---\n' % (msg.receive_time, msg.sender))
        f.write(text)
        f.write('\n')
        f.close()
        return '搞定！saved in history.txt'
    except Exception as e:
        return 'Exception: %s' % e

# 注意：优先匹配 后注册 的函数，且仅匹配 一个 注册函数。
@bot.register()
def default_msgproc(msg):
    logger.info('DEFAULT %s: %s, %s' % (msg.sender, msg.type, msg.text)) 
    logger.debug(vars(msg))

@bot.register(msg_types=SHARING)
def sharing_proc(msg):
    logger.debug('SHARING %s: %s, %s' % (msg.sender, msg.text, msg.url)) 

# 处理好友聊天信息
@bot.register(Friend, msg_types=TEXT, except_self=False)
def friends_msgproc(msg):
    logger.info('FRIEND %s: %s, %s' % (msg.sender, msg.type, msg.text)) 
    if (msg.sender == bot.self):
        logger.debug('msg.sender == bot.self')
        if msg.text.startswith('file'):
            #msg.sender.send_file('file.txt')
            return utils.execCmd('echo "hello"')
    if msg.text.startswith('...') or msg.text.startswith('。。。'):
        return '{} -> {}'.format(msg.sender, msg.text)     

# TODO: 这个只能被管理员调用，安全性
def robotQueryCommand(msg):
    logger.info('\nrobotQueryCommand %s: %s, %s' % (msg.sender, msg.type, msg.text))
    try: 
        cmdStr = re.sub(r'@[^! ]* *', "", msg.text) # MEMO：字符串替换
        logger.debug('cmdStr=%s' % cmdStr)
        # b'@\xe5\x88\x98\xe5\xbe\xb7 !#: ls'
        # b'@\xe5\x88\x98\xe5\xbe\xb7\xe2\x80\x85!#: ls'
        match = re.match(r'!(?P<code>.*?): (?P<text>.*)', cmdStr)
        #logger.debug(msg.text.encode())
        if match:
            logger.debug('matched' + str(match.groups()))
            code = match.group('code')
            text = match.group('text')
            logger.debug('code: ' + code)
            if (code == '#'):
                return utils.execCmd(text)
            elif (code == '+'):
                return appendMemo(msg, text)
            elif (code == '?'):
                return utils.getExpressStatus(text)
            elif (code == ''):
                return utils.execCmd("grep '%s' history.txt" % text)
            elif (code.isdigit()):
                return utils.execCmd("grep '%s' history.txt | head -n %s" % (text, code))
            else:
                return '命令格式为：!?: ***' # TODO
        elif cmdStr.isdigit(): # MEMO：判断是否为数字
            return utils.getExpressStatus(cmdStr)            
        elif cmdStr.startswith('file'):
            msg.sender.send_file('history.txt')
            pass
        elif cmdStr.startswith('...') or cmdStr.startswith('。。。'):
            return '{} -> {}'.format(msg.sender, msg.text)     
        else:
            return None # TODO
    except Exception as e:        
        return 'Exception: %s' % e

# 处理管理员聊天信息
admins = [bot.self] 
admins.append(ensure_one(bot.friends().search(nick_name='刘德')))
admins.append(ensure_one(bot.friends().search(nick_name='津')))
@bot.register(admins, msg_types=TEXT, except_self=False)
def admins_msgproc(msg):
    logger.info('ADMIN::TEXT %s: %s, %s' % (msg.sender, msg.type, msg.text)) 
    return robotQueryCommand(msg)

@bot.register(admins, msg_types=SHARING, except_self=False)
def admins_sharing_proc(msg):
    logger.info('ADMIN::SHARING %s: %s, %s' % (msg.sender, msg.text, msg.url)) 
    return robotQueryCommand(msg)

# 管理群内的消息处理
groups = []
#groups.append(ensure_one(bot.groups().search('水果吃货群')))
groups.append(ensure_one(bot.groups().search('津果机器人')))
@bot.register(groups, except_self=False)
def groups_msgproc(msg):
    #from_user = msg.member if isinstance(msg.chat, Group) else msg.sender
    logger.info('GROUP: sender=%s, member=%s, text=%s', msg.sender, msg.member, msg.text)
    if (msg.type == SHARING) and (msg.sender not in admin): 
        logger.warn('欢迎针对"水果吃法"进行讨论，请勿发表与群主题无关内容，谢谢')  # TODO: return
    if msg.is_at: # 自己被@时为True
        return robotQueryCommand(msg) # TODO: 避免群内太多@自己的消息
        return None
    return None

def get_new_member_name(msg):
    rp_new_member_name = (
        re.compile(r'^"(.+)"通过'),
        re.compile(r'邀请"(.+)"加入'),
        re.compile(r'^"(.+)" joined '),
        re.compile(r'invited "(.+)" to'),
    )
    
    for rp in rp_new_member_name:
        match = rp.search(msg.text)
        if match:
            return match.group(1)

# 新人入群的欢迎语
welcome_text = '''[Shake] 欢迎 @{} 入群！'''

@bot.register(groups, NOTE)
def welcome_msgproc(msg):
    # itchat 1.2.32 版本未格式化群中的 Note 消息
    from itchat.utils import msg_formatter
    msg_formatter(msg.raw, 'Text')
    
    name = get_new_member_name(msg)
    if name:
        return welcome_text.format(name)

embed()