#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 jeffZhuo
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement
from __future__ import nested_scopes
from __future__ import generators

import select

EPOLLIN = 0x001
EPOLLPRI = 0x002
EPOLLOUT = 0x004
EPOLLRDNORM = 0x040
EPOLLRDBAND = 0x080
EPOLLWRNORM = 0x100
EPOLLWRBAND = 0x200
EPOLLMSG = 0x400
EPOLLERR = 0x008
EPOLLHUP = 0x010
EPOLLONESHOT = (1 << 30)
EPOLLET = (1 << 31)

READ = EPOLLIN | EPOLLPRI | EPOLLRDNORM
WRITE = EPOLLOUT | EPOLLWRNORM
ERROR = EPOLLERR | EPOLLHUP | EPOLLMSG


class IOMultiplex(object):

    @classmethod
    def initialized(cls):
        pass

    def __init__(self):
        self.loop = _epoll()

        self._handler = {}

    def add_handler(self, fd, handler, eventmask):
        pass

    def remove_handler(self, fd):
        pass

    def start(self):
        pass



class _Select(object):

    def __init__(self):
        self.read_set = set()
        self.write_set = set()
        self.error_set = set()

    def register(self, fd, eventmask):
        if eventmask & READ:
            self.read_set.add(fd)
        elif eventmask & WRITE:
            self.write_set.add(fd)
        elif eventmask & ERROR:
            self.error_set.add(fd)

    def modify(self, fd, eventmask):
        if fd in self.read_set and (eventmask & READ) == False:
            self.read_set.remove(fd)

        if fd in self.write_set and (eventmask & WRITE) == False:
            self.read_set.remove(fd)

        if fd in self.error_set and (eventmask & ERROR) == False:
            self.read_set.remove(fd)

        self.register(fd, eventmask)

    def unregister(self, fd):
        if fd in self.read_set:
            self.read_set.remove(fd)

        if fd in self.write_set:
            self.read_set.remove(fd)

        if fd in self.error_set:
            self.read_set.remove(fd)

    def poll(self, timeout):
        read_list, write_list, error_list = select.select(self.read_set, self.write_set, self.error_set, timeout)

        events = {}

        for fd in read_list:
            events[fd] = events.get(fd, 0) | READ

        for fd in write_list:
            events[fd] = events.get(fd, 0) | WRITE

        for fd in error_list:
            events[fd] = events.get(fd, 0) | ERROR

        return events


if hasattr(select, "epoll"):
    _epoll = select.epoll()
elif hasattr(select, "poll"):
    _epoll = select.poll()
else:
    _epoll = _Select()