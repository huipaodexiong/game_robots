#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ProtoHandler.py   
@Contact :   512759438@qq.com
@Author  :   Jian
'''

from message import *
from util import HandlerBase

# 初始化
class ProtoHandler(HandlerBase):
    '''这里的方法都是被动触发的，只有在接收到协议包含了该方法就会自动触发'''
    def __init__(self, player=None):
        super(ProtoHandler, self).__init__(player)

# 登录协议返回处理
    def game_login(self,cls=Game_login):
        self.user_info = None
        self.player.hero_info = cls.hero_info
        if cls.code_str == 'OK' and cls.user:
            print(self.player.state_user_name,'登录成功')
            self.user_info = cls.user
            '''玩家初始属性获取'''
            self.player.player_id = self.user_info['id']
        else:
            self.player.send_msg(MSG_CREATE_PLAYER)

# 注册协议处理
    def game_register(self,cls=Game_register):
        if cls.user:
            self.user_info = cls.user
            '''玩家初始属性获取'''
            self.player.player_id = self.user_info['id']
            print(self.player.state_user_name, '创角成功')

# 检查角色初始化装备的ID和类型
    def user_bag_get_items(self,cls=User_bag_get_items):
        '''test_player_init_equip'''
        for item in cls.bag_items:
            item_id,item_type = item['item_id'],item['item_type']
            assert item_type == 3
            assert 300006 >= item_id >= 300001
