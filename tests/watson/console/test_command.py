# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.console.command import Base, find_commands_in_module
from tests.watson.console import support


class TestBaseCommand(object):

    @raises(TypeError)
    def test_init(self):
        Base()


class TestFindCommands(object):

    def test_find_commands(self):
        commands = find_commands_in_module(support)
        assert len(commands) == 7
