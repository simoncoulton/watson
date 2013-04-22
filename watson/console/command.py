# -*- coding: utf-8 -*-


class BaseCommand(object):
    """The base command that outlines the required structure for a console
    command.

    Help is automatically invoked when the `-h` or `--help` option is used.

    Usage:
        # can be executed by `script.py mycommand`
        class MyCommand(BaseCommand):
            name = 'mycommand'

            def execute(self):
                return True

        # can be executed by `script.py mycommand -t something`
        import optparse
        class MyCommand(BaseCommand):
            name = 'mycommand'
            options = [
                optparse.make_option('-t', help='Do something with -t')
            ]

            def execute(self):
                return True if self.parsed_options.t else False

        # can be executed by `script.py mycommand something`
        class MyCommand(BaseCommand):
            name = 'mycommand'
            arguments = [
                ('argument1', 'This is the help for the argument')
            ]

            def execute(self):
                return True if 'argument1' in self.parsed_args else False
    """
    name = None
    options = []
    arguments = []
    help = 'Missing help.'
    _parsed_args = None
    _parsed_options = None

    def __init__(self, *args):
        self.args = args

    @property
    def parsed_args(self):
        """Returns the parsed arguments.

        Returns:
            list|dict depending on whether or not there have been named arguments.
        """
        return self._parsed_args

    @parsed_args.setter
    def parsed_args(self, args):
        """Set the parsed arguments.
        """
        self._parsed_args = args

    @property
    def parsed_options(self):
        """Returns the parsed options.

        Returns:
            see optparse.parse_args() for more information.
        """
        return self._parsed_options

    @parsed_options.setter
    def parsed_options(self, options):
        """Set the parsed options.
        """
        self._parsed_options = options

    def execute(self):
        raise NotImplementedError('execute() must be implemented.')

    def __call__(self):
        return self.execute()
