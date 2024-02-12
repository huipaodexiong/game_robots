#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SendActor.py    
@Contact :   512759438@qq.com
@Author  :   Jian
'''

send Actor初始化
class SendActor(pykka.ThreadingActor):
    '''
    发送消息给服务端
    '''
    def __init__(self, player=None, sock=None):
        super(SendActor, self).__init__()
        self.player = player
        self.socket = sock
        self.wpe = 1


# 启动Send Actor
    def on_start(self):
        self.on_heart()

# 心跳包
    def on_heart(self):
        self.player.sys_count += 1
        if self.player.sys_count >= 590:
            self.actor_ref.tell({MSG_PROTO: {'cmd': 'hall_heart'}})
            self.player.sys_count = 0
        # 心跳这里时间会阻塞100毫秒
        self.actor_ref.tell({MSG_HEART:{'msg':'loop'}})
        time.sleep(0.1)

# 序列化和发送数据
    def on_receive(self, msg):
        '''
        msg[MSG_PROTO] 打包好的协议数据
        发送包有参数的为元组类型，没有参数则直接发送协议
        '''
        if MSG_PROTO in msg.keys() and msg[MSG_PROTO]:
            proto_id, proto_bin = msg[MSG_PROTO]['cmd'],msg[MSG_PROTO]
            proto_header = {
                'cmd': proto_id,
                'sessionId': self.wpe,
                'ts':int(time.time()*1000),
            }
            proto_header.update(proto_bin)
            buff = json.dumps(proto_header)
            self.socket.send(buff)
        elif msg[MSG_HEART]:
            self.on_heart()
        else:
            print('发过来空数据了')
        if self.wpe is XXX:
            self.wpe = 0
        else:
            self.wpe = self.wpe + 1

# 停止SendActor
    def on_stop(self):
        print('SendActor stop')
		
# log收集
    @GetLog(level='error')
    def on_failure(self, exception_type, exception_value, traceback):
        logging.error('SendActor fail => ', exception_type, exception_value, tb.print_tb(traceback))
