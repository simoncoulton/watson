# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.console.command import Base, find_commands_in_module
from tests.watson.console import support


class TestBaseCommand(object):
    def test_init(self):
        command = Base()
        assert not command.arguments

    @raises(NotImplementedError)
    def test_execute(self):
        command = Base()
        command()


class TestFindCommands(object):
    def test_find_commands(self):
        commands = find_commands_in_module(support)
        assert len(commands) == 6
