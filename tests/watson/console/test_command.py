# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.console.command import BaseCommand


class TestBaseCommand(object):
    def test_init(self):
        command = BaseCommand()
        assert not command.options

    @raises(NotImplementedError)
    def test_execute(self):
        command = BaseCommand()
        command()
