# -*- coding: utf-8 -*-
import argparse
from collections import OrderedDict
import os
import sys
from watson.common.imports import load_definition_from_string
from watson.console import colors, styles


class Runner(object):
    """A command line runner that allows new commands to be added and run on
    demand.

    Commands can be added either as a fully qualified name, or imported.

    Usage:
        runner = Runner(commands=['module.commands.ACommand'])
        runner()
    """
    _argv = None
    _name = None
    _commands = None

    def __init__(self, argv=None, commands=None):
        self._argv = argv or sys.argv[:]
        self._name = os.path.basename(self._argv.pop(0))
        self._commands = []
        if commands:
            self.add_commands(commands)

    @property
    def name(self):
        """Returns the name of the script that runner was executed from.
        """
        return self._name

    @property
    def commands(self):
        """A list of all commands added to the runner.

        Returns:
            OrderedDict containing all the commands.
        """
        commands = {}
        for command in self._commands:
            if isinstance(command, str):
                command = load_definition_from_string(command)
            commands[command.name] = command
        return OrderedDict(sorted(commands.items()))

    def add_command(self, command):
        """Convenience method to add new commands after the runner has been
        initialized.

        Args:
            string|class command: the command to add
        """
        self._commands.append(command)

    def add_commands(self, commands):
        """Convenience method to add multiple commands.

        Args:
            list|tuple commands: the commands to add
        """
        for command in commands:
            self.add_command(command)

    @property
    def usage(self):
        """Returns the usage text.

        This is used when the -h or --help command is invoked.
        """
        help = colors.header("""{name} [command], or append -h (--help) for additional help.
        """)
        return help.format(name=self.name)

    @property
    def available_commands_usage(self):
        """Returns the usage text for all commands.

        This is used when no commands have been specified.
        """
        help = '\n'.join([
            '{usage}',
            '',
            'Commands:\n    {commands}',
            ''
        ])
        commands = []
        for name, command in self.commands.items():
            commands.append('{0}: {1}'.format(styles.bold(name), command.help))

        return help.format(commands="\n    ".join(commands),
                           usage=self.usage)

    def get_command_usage(self, command):
        """Returns the usage string for an individual command.
        """
        usage = []
        for arguments in command.arguments:
            if isinstance(arguments, tuple):
                usage.append(''.join(('[', arguments[0][0], ']')))
            else:
                usage.append(arguments.get('name', arguments.get('dest')))
        return colors.header(' '.join((command.name, ' '.join(usage))))

    def get_command(self, command_name):
        """Returns an initialized command from the attached commands.
        """
        if command_name not in self.commands:
            return None
        return self.commands[command_name]()

    def execute(self):
        """Executes the specified command.
        """
        parser = ArgumentParser(add_help=False)
        help_args = ('-h', '--help')
        help = False
        command = None
        try:
            for help_arg in help_args:
                if help_arg in self._argv:
                    help = self._argv.pop(self._argv.index(help_arg))
            if self._argv:
                command = self.get_command(self._argv.pop(0))
                if command:
                    parser.add_arguments(command.arguments)
                    parser.description = command.help
                    parser.usage = self.get_command_usage(command)
        except:
            raise
        if not command:
            parser.usage = self.available_commands_usage
            help = True
        if help:
            parser.print_help()
        if command and not help:
            try:
                command.parsed_args = parser.parse_args(self._argv)
                return command()
            except ConsoleError as exc:
                sys.stderr.write(colors.fail('Error: {0}\n'.format(exc)))

    def __call__(self):
        return self.execute()


class ConsoleError(KeyError):
    """An error that should be raised from within the command.
    """
    pass


class ArgumentParser(argparse.ArgumentParser):
    def parse_known_args(self, args=None, namespace=None):
        args, argv = super(ArgumentParser, self).parse_known_args(args, namespace)
        return args, []

    def add_arguments(self, arguments_list):
        for arguments in arguments_list:
            if isinstance(arguments, tuple):
                args, arguments = arguments
            else:
                args = []
                if 'required' not in arguments:
                    arguments['nargs'] = '?'
            self.add_argument(*args, **arguments)
