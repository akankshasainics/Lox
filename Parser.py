from Expr import Expr, Binary, Unary, Literal, Grouping
from TokenType import tokenType
from Token import Token
from Error import Error
from Stmt import Stmt

class Parser:
    class ParseError(Exception):
        def __init__(self, message) -> None:
            super().__init__(message)

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens 
        self.current: int = 0

    def unary(self) -> Expr:
        while self.match(tokenType.BANG, tokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right) 
        return self.primary()

    def error(self, token: Token, message: str) -> ParseError:
        Error.errorToken(token, message)
        raise Parser.ParseError("Parsing error")

    def consume(self, type: tokenType, message: str):
        if self.check(type):
            return self.advance()
        self.error(self.peek(), message)

    def primary(self):
        if self.match(tokenType.FALSE):
            return Literal(False)
        if self.match(tokenType.TRUE):
            return Literal(True)
        if self.match(tokenType.NIL):
            return Literal(None)

        if self.match(tokenType.NUMBER, tokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(tokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(tokenType.RIGHT_PAREN, "Expect ) after expression")
            return Grouping(expr)

        return self.error(self.peek(), "Expect expression")

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(tokenType.STAR, tokenType.SLASH):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        while self.match(tokenType.MINUS, tokenType.PLUS):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()
        while self.match(tokenType.GREATER, tokenType.GREATER_EQUAL, tokenType.LESS, tokenType.LESS_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def isAtEnd(self):
        return self.peek().type == tokenType.EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()


    def check(self, type: tokenType):
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def match(self, *types: tokenType):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    

    def equality(self) -> Expr:
        expr: Expr = self.comparison()
        while self.match(tokenType.BANG_EQUAL, tokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def expression(self) -> Expr:
        return self.equality() 

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == tokenType.SEMICOLON:
                return
            startTokens = [tokenType.CLASS, tokenType.FUN, tokenType.VAR, tokenType.FOR, tokenType.IF, tokenType.WHILE, tokenType.PRINT, tokenType.RETURN]
            if self.peek().type in startTokens:
                return;
            self.advance()

    def expressionStatement(self) -> Stmt:
        pass

    def printStatement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(tokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def statement(self) -> Stmt:
        if self.match(tokenType.PRINT):
            return self.printStatement()
        return self.expressionStatement()

    def parse(self) -> Expr | None:
        try:
            # statements: list[Stmt] = []
            # while not self.isAtEnd():
            #     statements.append(self.statement())
            return self.expression()
        except Parser.ParseError:
            return None
