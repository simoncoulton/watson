# -*- coding: utf-8 -*-
from watson.console import ConsoleError
from watson.console import command


class NoCallCommand(command.Base):
    pass


class SampleNonStringCommand(command.Base):
    name = 'nonstring'
    help = 'Some help for SampleNonStringCommand'

    def execute(self):
        return True


class SampleStringCommand(command.Base):
    name = 'string'
    help = 'Some help for SampleStringCommand'

    def execute(self):
        raise ConsoleError('Something went wrong')


class SampleNoHelpNoExecuteCommand(command.Base):
    name = 'nohelpnoexecute'


class SampleOptionsCommand(command.Base):
    name = 'runoptions'
    help = 'Options command!'
    arguments = [
        (('-f', '--filename',), {'help': 'Use filename with command'}),
    ]

    def execute(self):
        if self.parsed_args.filename:
            return True
        return None


class SampleArgumentsCommand(command.Base):
    name = 'runargs'
    help = 'Arguments command!'
    arguments = [
        {'dest': 'argument1', 'help': 'the argument that needs to be passed'},
        {'dest': 'argument2', 'help': 'the second argument'}
    ]

    def execute(self):
        if 'argument2' in self.parsed_args:
            return True
        return False


class SampleArgumentsWithOptionsCommand(command.Base):
    name = 'runargsoptions'
    help = 'Arguments/Options command!'
    arguments = [
        (('-f', '--filename',),
         {'help': 'Use filename with command', 'required': False}),
        {'dest': 'argument1', 'help': 'the argument that needs to be passed'},
        {'dest': 'argument2', 'help': 'the second argument'},
    ]

    def execute(self):
        if 'argument1' in self.parsed_args and self.parsed_args.filename:
            return True
        return False
