#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   RemoteHandler.py   
@Contact :   512759438@qq.com
@Author  :   Jian
'''

# 初始化
class RemoteHandler(HandlerBase):
    '''
    添加方法时注意：
        定义调用方法时注明参数输入类型
        每个需要远程调用的方法都要加上data参数，在player.remote_msg方法定义method:str=None, data=None
    '''
    def __init__(self, player=None):
        super(RemoteHandler, self).__init__(player)
	
	# 传送数据到打包actor
    def send_msg(self, data=None):
        self.player.send_actor.tell({MSG_PROTO: data})
    # 传送数据到任务actor
    def task_msg(self, data=None):
        self.player.task_actor.tell({MSG_TASK:data})
    # 传送数据到活动actor
    def activity_msg(self,msg_type=None,data=None):
        self.player.activity_actor.tell({
            'msg':msg_type,
            'data':data})

    def send_gm(self,*args):
        '''
        设置玩家gm,输入类型指定为（*args:tuple) -> tuple
        self.send_gm('set hp 100')
        '''
        for case in list(args):
            self.send_msg(Game_gm_action().request(gm_type=None,gm_param=case))
			
# 填充指令-GM
	# 把添加道具GM封装
    def add_item(self,item_id,num):
        self.send_msg(Game_gm_action().request(gm_type=None,gm_param=f'add item {item_id} {num}'))
	# 设置玩家的属性
    def set_player_attr(self,data):
        '''
        构建指定数据的玩家
        '''
        self.send_gm('set attr 10086 30009')
        self.add_item(120008, 10000)
        self.add_item(130007, 10000)
        self.add_item(150006, 10000)
        self.add_item(190005, 10000)
        self.add_item(150014, 10000)

# 填充指令-技能使用
    def send_skill_fire_wall(self,data):
        '''使用火墙术
        蜈蚣洞
        '''
        scene_id = 20702
        direction = 8
        pos_list = self.skill_pos(60, 19, 10)
        if len(pos_list) > data:
            point = pos_list[data]
            flag = (0,'0')
            msg = C12003(scene_id,direction,20300,2,flag,point)
            self.send_msg(msg)

# 填充指令-进入某场景
    def enter_scene(self,scene_id,x,y):
        '''进入场景'''
        msg = C11082(scene_id, x, y, 0)
        self.send_msg(msg)

# 填充指令-抽奖活动
    def lottery(self,data=1):
        for _ in range(data):
            msg = C34006(1)
            self.send_msg(msg)

# 填充指令-玩家移动
    def player_move(self,target_x,target_y,direction=1):
        '''
        A星寻路
        :param target_x:
        :param target_y:
        :param direction: 朝向
        '''
        move_path = find_path(self.player.pos_x,self.player.pos_y,target_x,target_y)
        for case in _move_path:
            start_move = C11002(self.player.scene_id,direction,(case.x,case.y),(case.x+1,case.y+1))
            self.send_msg(start_move)
        # 移动完同步玩家位置
        self.player.pos_x,self.player.pos_y = move_path[-1].x,move_path[-1].y

# Remote使用例子
    def __call__(self, remote_fun:str='',*remote_args,remote_count:int=1):
        if isinstance(remote_fun,str):
            for _ in range(remote_count):
                self.proxy.remote_msg(remote_fun,remote_args)
        else:raise TypeError('调用方法名为字符串格式')

