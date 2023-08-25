#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 17:14
# @Author  : 雷雨
# @File    : message.py
# @Desc    :
from queue import Queue
from typing import Any, Iterable

from pydantic import BaseModel, Field

from complements import interaction


class Message(BaseModel):
    origin: 'Role'
    to: 'Role'
    message: Any
    interaction_type: str = Field(enum=interaction.InteractionType)


class MessageQueue:

    def __init__(self):
        self.queue = Queue()

    def get(self) -> Iterable[Message]:
        yield self.queue.get()

    def put(self, message: Message):
        self.queue.put(message)


# class FeiShu:
#
#     def __init__(self):
#         self.queue = Queue()
#
#     def get(self) -> Iterable[Message]:
#         yield ''
#
#     def put(self, message: Message):
#         ...
