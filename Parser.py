from Expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign
from TokenType import tokenType
from Token import Token
from Error import Error
from Stmt import Stmt, Print, Expression, Var, Block, If

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

        if self.match(tokenType.IDENTIFIER):
            return Variable(self.previous())

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

    def assignment(self) -> Expr:
        expr: Expr = self.equality()
        if self.match(tokenType.EQUAL):
            equals: Token = self.previous()
            value: Expr = self.assignment()
            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def expression(self) -> Expr:
        return self.assignment() 

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
        expr: Expr = self.expression() 
        self.consume(tokenType.SEMICOLON, "Expect ; after expression")
        return Expression(expr)

    def printStatement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(tokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def block(self) -> Stmt:
        statements = []
        while not self.check(tokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        self.consume(tokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
    
    def ifStatement(self) -> Stmt:
        self.consume(tokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition: Expr = self.expression()
        self.consume(tokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch: Stmt = self.statement()
        elseBranch: Stmt = None
        if self.match(tokenType.ELSE):
            elseBranch = self.statement()
        
        return If(condition, thenBranch, elseBranch) 


    def statement(self) -> Stmt:
        if self.match(tokenType.PRINT):
            return self.printStatement()
        if self.match(tokenType.LEFT_BRACE):
            return Block(self.block())
        if self.match(tokenType.IF):
            return self.ifStatement()
        return self.expressionStatement()

    def varDeclaration(self) -> Stmt:
        name: Token = self.consume(tokenType.IDENTIFIER, "Expect variable name.")
        initializer: Expr = None
        if self.match(tokenType.EQUAL):
            initializer = self.expression()
        self.consume(tokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def declaration(self) -> Stmt:
        try:
            if self.match(tokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except Parser.ParseError as e:
            self.synchronize()
            return None

    def parse(self) -> list[Stmt]:
        try:
            statements: list[Stmt] = []
            while not self.isAtEnd():
                statements.append(self.declaration())
            return statements
        except Parser.ParseError:
            return None
