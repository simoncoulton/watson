# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.console import Runner, ConsoleError
from tests.watson.console.support import SampleNonStringCommand


class TestConsoleError(object):
    def test_instance(self):
        exc = ConsoleError()
        assert isinstance(exc, KeyError)


class TestRunner:
    def test_create(self):
        runner = Runner(['test.py'], commands=[
            'tests.watson.console.support.SampleStringCommand',
            SampleNonStringCommand
        ])
        assert len(runner.commands) == 2
        assert runner.name == 'test.py'

    def test_add_commands(self):
        runner = Runner()
        assert len(runner.commands) == 0
        runner.add_commands([SampleNonStringCommand, 'tests.watson.console.support.SampleStringCommand'])
        assert len(runner.commands) == 2

    @raises(TypeError)
    def test_no_execute(self):
        runner = Runner(['test.py', 'nohelpnoexecute'], commands=[
            'tests.watson.console.support.SampleNoHelpNoExecuteCommand'
        ])
        runner.execute()

    def test_execute_usage(self):
        runner = Runner(['test.py'], commands=[
            'tests.watson.console.support.SampleStringCommand',
            SampleNonStringCommand
        ])
        output = runner.execute()  # will print to screen in tests
        assert not output

    def test_execute_command_usage(self):
        runner = Runner(['test.py', 'nonstring', '-h'], commands=[
            'tests.watson.console.support.SampleStringCommand',
            SampleNonStringCommand
        ])
        output = runner.execute()  # will print to screen in tests
        assert not output

    def test_execute_command_usage_with_args(self):
        runner = Runner(['test.py', 'runargs', '-h'], commands=[
            'tests.watson.console.support.SampleArgumentsCommand'
        ])
        output = runner.execute()  # will print to screen in tests
        assert not output

    def test_execute_command_usage_with_options(self):
        runner = Runner(['test.py', 'runoptions', '-h'], commands=[
            'tests.watson.console.support.SampleOptionsCommand'
        ])
        output = runner.execute()  # will print to screen in tests
        assert not output

    def test_execute_command_with_options_invalid(self):
        runner = Runner(['test.py', 'runoptions', '-d'], commands=[
            'tests.watson.console.support.SampleOptionsCommand'
        ])
        output = runner.execute()  # will print to screen in tests
        assert not output

    def test_execute_command_with_error(self):
        runner = Runner(['test.py', 'string'], commands=[
            'tests.watson.console.support.SampleStringCommand'
        ])
        runner()

    def test_execute_command(self):
        runner = Runner(['test.py', 'nonstring'], commands=[
            'tests.watson.console.support.SampleNonStringCommand'
        ])
        assert runner()

    def test_execute_command_with_options(self):
        runner = Runner(['test.py', 'runoptions', '-f', 'test'], commands=[
            'tests.watson.console.support.SampleOptionsCommand'
        ])
        output = runner.execute()  # will print to screen in tests
        assert output

    def test_execute_command_with_args(self):
        runner = Runner(['test.py', 'runargs', 'test', 'test2'], commands=[
            'tests.watson.console.support.SampleArgumentsCommand'
        ])
        output = runner.execute()  # will print to screen in tests
        assert output

    def test_execute_command_with_args_options(self):
        runner = Runner(['test.py', 'runargsoptions', 'test', '-f', 'filename.txt'], commands=[
            'tests.watson.console.support.SampleArgumentsCommand',
            'tests.watson.console.support.SampleArgumentsWithOptionsCommand'
        ])
        output = runner.execute()  # will print to screen in tests
        assert output
