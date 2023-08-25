#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:51
# @Author  : 雷雨
# @File    : interaction.py
# @Desc    :
from enum import Enum


class InteractionType(Enum, str):
    dialog = 'dialog'
    conference = 'conference'


class Dialog:
    roles = []


class Conference:
    roles = []
