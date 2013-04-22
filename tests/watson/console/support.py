# -*- coding: utf-8 -*-
import optparse
from watson.console import ConsoleError
from watson.console.command import BaseCommand


class SampleNonStringCommand(BaseCommand):
    name = 'nonstring'
    help = 'Some help for SampleNonStringCommand'

    def execute(self):
        return True


class SampleStringCommand(BaseCommand):
    name = 'string'
    help = 'Some help for SampleStringCommand'

    def execute(self):
        raise ConsoleError('Something went wrong')


class SampleNoHelpNoExecuteCommand(BaseCommand):
    name = 'nohelpnoexecute'


class SampleOptionsCommand(BaseCommand):
    name = 'runoptions'
    help = 'Options command!'
    options = [
        optparse.make_option('-f', '--filename', help='Use filename with command')
    ]

    def execute(self):
        if self.parsed_options.filename:
            return True
        return None


class SampleArgumentsCommand(BaseCommand):
    name = 'runargs'
    help = 'Arguments command!'
    arguments = [
        ('argument1', 'the argument that needs to be passed'),
        ('argument2', 'the second argument')
    ]

    def execute(self):
        if 'argument2' in self.parsed_args:
            return True
        return False


class SampleArgumentsWithOptionsCommand(BaseCommand):
    name = 'runargsoptions'
    help = 'Arguments/Options command!'
    arguments = [
        ('argument1', 'the argument that needs to be passed'),
        ('argument2', 'the second argument')
    ]
    options = [
        optparse.make_option('-f', '--filename', help='Use filename with command')
    ]

    def execute(self):
        if 'argument1' in self.parsed_args and self.parsed_options.filename:
            return True
        return False
