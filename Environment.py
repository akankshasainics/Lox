from Token import Token
from RunTimeException import RunTimeException

class Environment:
    def __init__(self, enclosing = None) -> None:
        self.values: dict = {}
        self.enclosing: Environment = enclosing

    def define(self, name: str, value: object):
        self.values[name] = value

    def assign(self, name:  Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        raise RunTimeException(name, "Undefined variable '" + name.lexeme + "'.")

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RunTimeException(name, "Undefined variable '" + name.lexeme + "'.")
