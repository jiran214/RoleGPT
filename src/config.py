#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:46
# @Author  : 雷雨
# @File    : config.py
# @Desc    :
from pathlib import Path


class Config:
    root_path = Path(__file__).parent
    knowledge_path = (root_path.parent / 'knowledge').absolute()
    api_key_list = [
        'xxxxx'
    ]
    api_key = ''
