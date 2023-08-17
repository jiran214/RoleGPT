#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 17:14
# @Author  : 雷雨
# @File    : message.py
# @Desc    :
from typing import Any, Iterable

from pydantic import BaseModel
from roles.base import Role


class Message(BaseModel):
    origin: Role
    to: Role
    message: Any


class MessageQueue:

    def __init__(self):
        self.queue = []

    def get(self) -> Iterable[Message]:
        yield ''

    def put(self, message: Message):
        ...
