from Token import Token
from RunTimeException import RunTimeException

class Environment:
    def __init__(self) -> None:
        self.values: dict = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def assign(self, name:  Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        raise RunTimeException(name, "Undefined variable '" + name.lexeme + "'.")

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise RunTimeException(name, "Undefined variable '" + name.lexeme + "'.")
