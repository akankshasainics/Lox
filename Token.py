from TokenType import tokenType

class Token:
    def __init__(self, type: tokenType, lexeme: str,literal: object,line: int ) -> None:
        self.type: tokenType = type
        self.lexeme: str = lexeme
        self.line: int = line
        self.literal: object = literal

    def toString(self):
        return str(self.type) + " " + self.lexeme + " " + str(self.literal)

