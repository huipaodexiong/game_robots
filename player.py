#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   player.py    
@Contact :   512759438@qq.com
@Author  :   Jian
'''


import pykka
import websocket
import traceback as tb
from proto import ProtoHandler
from remote import RemoteHandler
from util import MsgSwitch, RecvActor, SendActor


TEST_CASE_CALL = None
class Player(pykka.ThreadingActor):
    def __init__(self, user_name='', server='SERVER_1',sex=1, job=1):
        super(Player, self).__init__()
        self.host = SERVER_LIST[server]['GAME_HOST']
        self.port = SERVER_LIST[server]['GAME_PORT']
        self.web_host = "x.x.x.x"
        self.recv_actor = None
        self.send_actor = None
        self.socket = None
        self.proto_handler = ProtoHandler(self)
        self.remote_handler = RemoteHandler(self)
        '''测试用例执行时需要调用player'''
        global TEST_CASE_CALL
        TEST_CASE_CALL = self

        self.player_id = None
        self.state_user_id = 0
        self.state_user_name = user_name
        self.sys_count = 0

# 封装消息发送，用来给自己发送消息或者其他Actor调用
    def send_msg(self, msg_type=None, data=None):
        '''
        :param msg_type:消息类型 
        :param data: 数据
        '''
        self.actor_ref.tell({
            'msg': msg_type,
            'data': data
        })

# Player Actor实例化之后第一个执行的地方
# 接下来就把消息告诉自己，on_receive会接收到这条消息
   	def on_start(self):
        if self.state_user_name is '':
            self.send_msg(MSG_GUEST_LOGIN)
        else:
            self.send_msg(MSG_LOGIN_INFO)

# 接收消息及消息处理
    def on_receive(self, msg):
        for case in MsgSwitch(msg):
            # 获取用户信息
            if case(MSG_LOGIN_INFO):
                account_info = Account(self.state_user_name).login_info()
                if account_info['code_str'] == 'OK':
                    user_into = account_info['user']
                    self.create_player_params  = {
                        'rd3_token': user_into['token'],
                        'rd3_userId': user_into['userId'],
                        'server_list_type': 0,
                        'sid': 1,
                        'token': user_into['token'],
                    }
                    self.create_player_params.update(Account(self.state_user_name).data)
                    self.create_player_params.pop('password')
                    self.create_player_params['cmd'] = 'game_login'
                    self.send_msg(MSG_LOGIN)
                else:print(f'获取角色信息ERROR, 原因: {account_info["code_str"]},{account_info["code"]}')
                break

            # 用户登录
            if case(MSG_LOGIN):
                self.socket = websocket.create_connection(f'ws://{self.host}:{self.port}/')
                self.recv_actor = RecvActor.start(self, self.socket)
                self.send_actor = SendActor.start(self, self.socket)
                self.send_actor.tell({MSG_PROTO: self.create_player_params})
                break
            # 用户创角
            if case(MSG_CREATE_PLAYER):
                create_data = {
                    'nickname': self.state_user_name,
                    'rd3_token': self.create_player_params['rd3_token'],
                    'rd3_userId': self.create_player_params['rd3_userId'],
                    'sid': self.create_player_params['sid'],
                    'token': self.create_player_params['token'],
                }
                self.send_actor.tell({MSG_PROTO: create_data})
                break

            # 服务端返回协议处理
            if case(MSG_PROTO):  
                method, data = msg['data']
                if hasattr(self.proto_handler, method):
                    getattr(self.proto_handler, method)(data)
                else:
                    print(f"没有为协议: {method} 定义处理方法, 请前往 proto.py 文件中定义!")
                break
            # 控制台调用命令
            if case(MSG_REMOTE_CMD):
                method = msg['method']
                method = (type(method) is int and "r" + str(method)) or (type(method) is str and method)
                if hasattr(self.remote_handler, method):
                    getattr(self.remote_handler, method)(msg['data'])
                else:
                    print(f"没有为远程命令: {method} 定义处理方法, 请前往 remote.py 文件中定义!")
                break

#封装远程命令
    def remote_msg(self, method:str=None, data=None):
        '''
        调用remote里的方法
        :param method: 方法名
        :param data: 传入的参数 元组
        '''
        self.actor_ref.tell({
            'msg': MSG_REMOTE_CMD,
            'method': method,
            'data': data
        })

# 停止Player Actor，先停止其他的Actor再关闭socket，最后关掉自己
	def on_stop(self):
        self.recv_actor.stop()
        self.send_actor.stop()
        self.socket.close()
        self.socket.shutdown()
        self.stop()

# log收集
	    # 打印报错消息
    @GetLog(level='fatal')
    def on_failure(self, exception_type, exception_value, traceback):
        logging.fatal(f'Player: {self.state_user_name} is down.')
        logging.fatal(f"ErrorType  => {exception_type}")
        logging.fatal(f"ErrorValue => {exception_value}")
        logging.fatal(f"TraceBack  => {tb.print_tb(traceback)}")
        self.on_stop()
