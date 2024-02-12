#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setting.py   
@Contact :   512759438@qq.com
@Author  :   Jian
'''

import pathlib
import logging
import re
import ijson
from ruamel import yaml
from openpyxl import load_workbook


# 加载配置文件
'''
BASE_DIR = pathlib.Path(__file__).parent.parent
MESSAGE_PATH = BASE_DIR / 'config' / 'message.yaml'
PROP_PATH = BASE_DIR / 'config' / 'propConfig.yaml'
SUNDRY_PATH = BASE_DIR / 'config' / 'sundry.yaml'
SERVER_PATH = BASE_DIR / 'config' / 'serverList.yaml'
'''

# 加载数据库
redis_client = Redis.from_url('redis://127.0.0.1:6379/0', db='player')


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='playerDebug.log', level=logging.DEBUG, format=LOG_FORMAT, filemode='w')


class GetLog:
    def __init__(self, level='debug'):
        self.level = level

    def __call__(self, func):  # 接受函数
        def wrapper(*args, **kwargs):
            # logging.debug(func.__name__)
            getattr(logging, self.level)(func.__name__)
            func(*args, **kwargs)

        return wrapper


def get_hero_list():
    file_path = pathlib.Path(__file__).parent / 'testCaseFile' / 'HeroConfig.json'
    with open(file_path,'r', encoding='utf-8') as file:
        hero_id_list = []
        data = ijson.items(file,'')
        for hero_dict in list(data):
            for k,v in hero_dict.items():
                hero_id_list.append(v['id'])
        return hero_id_list


def get_config(yaml_file):
    BASE_DIR = pathlib.Path(__file__).parent
    with open(BASE_DIR / 'config' / f'{yaml_file}', 'r', encoding='utf-8') as file:
        data = yaml.load(file.read(), Loader=yaml.Loader)
        return data


## 加载配置文件
sundry_config = get_config('sundry.yaml')
server_config = get_config('serverList.yaml')