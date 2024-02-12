#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   RecvActor.py    
@Contact :   512759438@qq.com
@Author  :   Jian
'''

# RecvActor初始化
class RecvActor(pykka.ThreadingActor):
    def __init__(self, player=None, sock=None):
        super(RecvActor, self).__init__()
        self.player = player
        self.socket = sock

# 启动RecvActor
    def on_start(self):
        self.on_loop()

# 持续接收服务端数据
    def on_receive(self, msg):
        self.on_loop()
        self.actor_ref.tell({'msg': 'loop'})

# 接收服务端数据进行反序列化
    def on_loop(self):
        data = self.socket.recv()
        data = list(ijson.items(data,''))[0]
        proto_id,proto_bin = data['cmd'],data
        proto_module = protoFile
        proto_cls = getattr(proto_module, str(proto_id).capitalize())
        proto_cls_ins = proto_cls()
        if hasattr(proto_cls_ins, 'response'):
            getattr(proto_cls_ins,'response')(proto_bin)
            self.player.send_msg(MSG_PROTO, (proto_id, proto_cls_ins))
        else:
            self.player.send_msg(MSG_PROTO, (proto_id, proto_cls_ins))

# 停止RecvActor
    def on_stop(self):
        print('RecvActor stop')

# log收集
    @GetLog(level='error')
    def on_failure(self, exception_type, exception_value, traceback):
        logging.error(f'RecvActor fail -> {exception_type, exception_value, tb.print_tb(traceback)}')
