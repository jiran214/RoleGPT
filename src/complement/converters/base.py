#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 17:50
# @Author  : 雷雨
# @File    : base.py
# @Desc    :
import abc
from typing import Any


class Converter(abc.ABC):

    @abc.abstractmethod
    def convert(self, data: Any):
        # 异步处理
        data = ''
        return data