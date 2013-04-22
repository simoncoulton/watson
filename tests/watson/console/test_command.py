# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.console.command import BaseCommand, find_commands_in_module
from tests.watson.console import support


class TestBaseCommand(object):
    def test_init(self):
        command = BaseCommand()
        assert not command.options

    @raises(NotImplementedError)
    def test_execute(self):
        command = BaseCommand()
        command()


class TestFindCommands(object):
    def test_find_commands(self):
        commands = find_commands_in_module(support)
        assert len(commands) == 6
