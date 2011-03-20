""" Shell."""

import sys
import copy

import sqlparse
from rl import completer as rlcompleter
from rl import completion as rlcompletion

__all__ = ["Shell"]

class Shell(object):

    def __init__(self, connection, prompt="#"):
        self.connection = connection
        self.prompt = prompt
        self._buffer = _Buffer()

    def run(self):

        rlcompleter.parse_and_bind("TAB: complete")
        rlcompleter.completer = self.complete

        while True:
            try:
                self._buffer.add_line(raw_input(self.prompt + " "))
            except (EOFError, KeyboardInterrupt), e:
                break

        self.exit()

    def exit(self):
        # TODO: Better move that to parametrized callback.
        sys.exit(0)

    def complete(self, _text, _state):
        buffer = self._buffer.copy()
        buffer.add_line(rlcompletion.line_buffer)

class _Buffer(object):

    def __init__(self, statements=None, lines=None, current_statement=None):
        self.statements = statements or []
        self.lines = lines or []
        self.current_statement = current_statement or None

    def add_statement(self, line):
        self.statements.append(sqlparse.parse(line))

    def add_line(self, line):
        splitted = sqlparse.split(line)
        for line in splitted:
            lines = self.lines + [line]
            if line.strip().endswith(";"):
                self.statements.append(sqlparse.parse("\n".join(lines))[0])
                self.lines = []
                self.current_statement = None
            else:
                self.lines = lines
                self.current_statement = sqlparse.parse("\n".join(lines))[0]

    @property
    def is_ready_for_exec(self):
        return bool(self.statements)

    def copy(self):
        statements = copy.deepcopy(self.statements)
        lines = copy.deepcopy(self.lines)
        current_statement = copy.deepcopy(self.current_statement)
        return _Buffer(statements, lines, current_statement)
