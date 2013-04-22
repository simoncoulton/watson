# -*- coding: utf-8 -*-
from collections import OrderedDict
import optparse
import os
import sys
from watson.common.imports import load_definition_from_string


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
        help = """Usage: {name} [subcommand], or append -h (--help) for additional help.
        """
        return help.format(name=self.name)

    @property
    def available_commands_usage(self):
        """Returns the usage text for all commands.

        This is used when no commands have been specified.
        """
        help = """{usage}
Commands:
    {commands}
"""
        commands = []
        for name, command in self.commands.items():
            commands.append('{0}: {1}'.format(name, command.help))

        return help.format(commands="\n    ".join(commands),
                           usage=self.usage)

    def get_command_usage(self, command):
        help = """Usage: {name} {command} {arguments_list}

Arguments:
{arguments}
"""
        if command.arguments:
            arguments_list = []
            arguments_help_list = []
            for argument, help_text in command.arguments:
                arguments_list.append('[{0}]'.format(argument))
                arguments_help_list.append('    {0}: {1}\n'.format(argument, help_text))
            return help.format(name=self.name,
                               command=command.name,
                               arguments="".join(arguments_help_list),
                               arguments_list=' '.join(arguments_list))
        else:
            help = """{name} {command}
{help}
"""
            return help.format(name=self.name, command=command.name,
                               help=command.help)

    def get_command(self, command_name):
        return self.commands[command_name]()

    def execute(self):
        parser = NoInvalidOptionParser(add_help_option=False)
        _help_options = ('-h', '--help')
        command = None
        help_index = -1
        try:
            # shift the -h to the end so command is the first index
            for _help in _help_options:
                if _help in self._argv:
                    help_index = self._argv.index(_help)
            if help_index >= 0:
                self._argv.pop(help_index)
            command_name = self._argv.pop(0)
            command = self.get_command(command_name)
            if command.options:
                parser.add_options(command.options)
            parser.usage = self.get_command_usage(command)
            if help_index >= 0:
                parser.print_help()
        except:
            pass  # no command, and no help
        if not command:
            sys.stdout.write(self.available_commands_usage)

        (options, args) = parser.parse_args(self._argv)
        if command and help_index < 0:
            try:
                if command.arguments:
                    command.parsed_args = {}
                    i = 0
                    for argument, help in command.arguments:
                        try:
                            command.parsed_args[argument] = args[i]
                        except:
                            pass
                        i = i+1
                else:
                    command.parsed_args = args
                command.parsed_options = options
                return command()
            except ConsoleError as exc:
                sys.stdout.write('Error: {0}\n'.format(exc))

    def __call__(self):
        return self.execute()


class ConsoleError(KeyError):
    """An error that should be raised from within the command.
    """
    pass


class NoInvalidOptionParser(optparse.OptionParser):
    def _process_args(self, largs, rargs, values):
        # override the _process_args to prevent errors if no option found.
        try:
            while rargs:
                arg = rargs[0]
                if arg == "--":
                    del rargs[0]
                    return
                elif arg[0:2] == "--":
                    self._process_long_opt(rargs, values)
                elif arg[:1] == "-" and len(arg) > 1:
                    self._process_short_opts(rargs, values)
                elif self.allow_interspersed_args:
                    largs.append(arg)
                    del rargs[0]
                else:
                    return
        except:
            largs.append(arg)
