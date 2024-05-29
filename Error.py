from Token import Token
from TokenType import tokenType
class Error:
    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print("[line {line}] Error {where} : {message}".format(line = line, where = where, message  = message))

    @staticmethod
    def error(line: int, message: str) -> None:
        Error.report(line, "", message)

    @staticmethod
    def errorToken(token: Token, message: str) -> None:
        if token.type == tokenType.EOF:
            Error.report(token.line, " at end ", message)
        else:
            Error.report(token.line, " at '" + token.lexeme + "'", message)