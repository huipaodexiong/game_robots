#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   MsgSwitch.py   
@Contact :   512759438@qq.com
@Author  :   Jian
'''

# 初始化
class MsgSwitch:
    def __init__(self, msg):
        self.value = msg
        self.fall = False
		
    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif type(self.value) is dict and self.value.get('msg') in args:
            self.fall = True
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

