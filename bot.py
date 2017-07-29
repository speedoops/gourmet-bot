#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import logging.config
import wxpy
import utils

def setup_logging(
    default_path='logging.json', 
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration
 
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        import json
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# 初始化日志
setup_logging()
LOG = logging.getLogger(__name__)


# 初始化机器人
def on_logout():
    import time
    # http://blog.csdn.net/caisini_vc/article/details/5619954
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    LOG.warn('---\nlogged out on %s\n---' %
             time.strftime(ISOTIMEFORMAT, time.localtime()))
    os._exit(0)

# 初始化机器人对象
bot = wxpy.Bot('wxpy_cache.pkl', console_qr=True, logout_callback=on_logout)




@bot.register()
def default_msgproc(msg):
    """ 默认消息处理函数。
    注意：优先匹配 后注册 的函数，且仅匹配 一个 注册函数。 
    """
    LOG.info('DEFAULT %s: %s, %s' % (msg.sender, msg.type, msg.text))
    #LOG.debug(vars(msg))


@bot.register(msg_types=wxpy.SHARING)
def sharing_msgproc(msg):
    LOG.debug('SHARING %s: %s, %s' % (msg.sender, msg.text, msg.url))


@bot.register(wxpy.Friend, msg_types=wxpy.TEXT, except_self=False)
def friends_msgproc(msg):
    """ 处理好友聊天信息 """
    LOG.info('FRIEND %s: %s, %s' % (msg.sender, msg.type, msg.text))
    if (msg.sender == bot.self):
        LOG.debug('msg.sender == bot.self')
        if msg.text.startswith('file'):
            # msg.sender.send_file('file.txt')
            return utils.execCmd('echo "hello"')
    if msg.text.startswith('...') or msg.text.startswith('。。。'):
        return '{} -> {}'.format(msg.sender, msg.text)


@bot.register(wxpy.Friend, msg_types=wxpy.ATTACHMENT, except_self=False)
def friends_fileproc(msg):
    LOG.info('FRIEND %s: %s, %s' % (msg.sender, msg.type, msg.text))
    msg.get_file('.')

# TODO: 这个只能被管理员调用，安全性


def robotQueryCommand(msg):
    LOG.info('robotQueryCommand %s: %s, %s',
             msg.sender, msg.type, msg.text)
    try:
        cmdStr = re.sub(r'@[^ \u2005]*[ \u2005]*', "", msg.text)  # MEMO：字符串替换
        LOG.debug('remove at, cmdStr=%s', cmdStr)
        # b'@\xe5\x88\x98\xe5\xbe\xb7 !#: ls'
        # b'@\xe5\x88\x98\xe5\xbe\xb7\xe2\x80\x85!#: ls'
        match = re.match(r'!(?P<code>.*?):[ ]*(?P<text>.*)', cmdStr, re.DOTALL)
        # logger.debug(msg.text.encode())
        if match:
            LOG.debug('matched' + str(match.groups()))
            code = match.group('code')
            text = match.group('text')
            LOG.debug('code: ' + code)
            if (code == '#'):
                return utils.execCmd(text)
            elif (code == '+'):
                return utils.appendMemo(msg, text)
            elif (code == '?'):
                return utils.replace_with_statuses(text)
            elif (code == ''):
                #return utils.execCmd("grep '%s' history.txt" % text)
                return utils.execCmd("sed -n '/^[^；]*$/d; s/^.*：//; s/。.*//; /.*%s.*/p' history.txt | uniq -u" % text)
            elif (code.isdigit()):
                #return utils.execCmd("sed -n '/^[^；]*$/d; s/^.*：//; s/。.*//; /.*%s.*/p' history.txt | uniq -u | head -n %s" % (text, code))
                return utils.execCmd("grep '%s' history.txt | head -n %s" % (text, code))
            elif (code == '*'):
                return utils.replace_with_addresses(text)
            elif (code == 'f'):
                msg.sender.send_file(text)
            else:
                return '命令格式错误，请输入？？？查询帮助'
        elif cmdStr.isdigit():  # MEMO：判断是否为数字
            return utils.get_shipment_status(cmdStr)
        elif cmdStr.startswith('file'):
            msg.sender.send_file('history.txt')
            pass
        elif cmdStr.startswith('???') or cmdStr.startswith('？？？'):
            return ''' 帮助，支持的命令格式如下：

!+: 记录内容 => 添加记录
!1: 关键词 => 按关键词查询记录
!: 关键词 => 按关键词查询，返回多条地址信息（相同的地址信息合并）
!*: 多行文本 => 批量将{姓名}替换为地址
!?: 多行文本 => 批量查询快递单
!f: 文件名 => 调试命令：获取系统文件
!#: 系统命令 => 调试命令：执行系统命令
                '''
        elif cmdStr.startswith('...') or cmdStr.startswith('。。。'):
            return '{} -> {}'.format(msg.sender, msg.text)
        else:
            LOG.debug('not matched: %s', cmdStr[:10].encode('utf_8') )
            return None  # TODO
    except Exception as e:
        LOG.exception(e)
        return 'Exception: %s' % e


# 处理管理员聊天信息
admins = [bot.self]
admins.append(wxpy.ensure_one(bot.friends().search(nick_name=u'刘德')))
admins.append(wxpy.ensure_one(bot.friends().search(nick_name=u'津')))


@bot.register(admins, msg_types=wxpy.TEXT, except_self=False)
def admins_msgproc(msg):
    LOG.info('ADMIN::TEXT %s: %s, %s' % (msg.sender, msg.type, msg.text))
    return robotQueryCommand(msg)


@bot.register(admins, msg_types=wxpy.SHARING, except_self=False)
def admins_sharing_proc(msg):
    LOG.info('ADMIN::SHARING %s: %s, %s' % (msg.sender, msg.text, msg.url))
    return robotQueryCommand(msg)


# 管理群内的消息处理
groups = []
# groups.append(wxpy.ensure_one(bot.groups().search(u'水果吃货群')))
groups.append(wxpy.ensure_one(bot.groups().search(u'津果机器人')))


@bot.register(groups, except_self=False)
def groups_msgproc(msg):
    #from_user = msg.member if isinstance(msg.chat, Group) else msg.sender
    LOG.info('GROUP: sender=%s, member=%s, text=%s',
             msg.sender, msg.member, msg.text)
    if (msg.type == wxpy.SHARING) and (msg.sender not in admins):
        LOG.warn('欢迎针对"水果吃法"进行讨论，请勿发表与群主题无关内容，谢谢')  # TODO: return
    if msg.is_at:  # 自己被@时为True
        return robotQueryCommand(msg)
    elif (msg.sender == bot.self):
        return robotQueryCommand(msg)
    else:
        LOG.debug('sender:%s != self:%s', msg.sender.user_name, bot.self.user_name)
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


@bot.register(groups, wxpy.NOTE)
def welcome_msgproc(msg):
    # itchat 1.2.32 版本未格式化群中的 Note 消息
    from itchat.utils import msg_formatter
    msg_formatter(msg.raw, 'Text')

    name = get_new_member_name(msg)
    if name:
        return welcome_text.format(name)


wxpy.embed()
