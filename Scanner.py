from TokenType import tokenType
from Token import Token
from Error import Error

class Scanner:
    keywords = {
        "and": tokenType.AND,
        "class": tokenType.CLASS,
        "else": tokenType.ELSE,
        "false": tokenType.FALSE,
        "for": tokenType.FOR,
        "fun":tokenType.FUN,
        "if": tokenType.IF,
        "nil": tokenType.NIL,
        "or": tokenType.OR,
        "print": tokenType.PRINT,
        "return": tokenType.RETURN,
        "super": tokenType.SUPER,
        "this": tokenType.THIS,
        "true": tokenType.TRUE,
        "var": tokenType.VAR,
        "while": tokenType.WHILE
    }

    def __init__(self, source) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self) -> list[Token]:
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(tokenType.EOF, "", None, self.line))
        return self.tokens

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanToken(self):
        c = self.advance()
        if c == "(":
            self.addToken(tokenType.LEFT_PAREN)
        elif c == ")":
            self.addToken(tokenType.RIGHT_PAREN)
        elif c == "{":
            self.addToken(tokenType.LEFT_BRACE)
        elif c == "}":
            self.addToken(tokenType.RIGHT_BRACE)
        elif c == ",":
            self.addToken(tokenType.COMMA)
        elif c == ".":
            self.addToken(tokenType.DOT)
        elif c == "-":
            self.addToken(tokenType.MINUS)
        elif c == "+":
            self.addToken(tokenType.PLUS)
        elif c == ";":
            self.addToken(tokenType.SEMICOLON)
        elif c == "*":
            self.addToken(tokenType.STAR)
        elif c == "!":
            self.addToken(tokenType.BANG_EQUAL if self.match("=") else tokenType.BANG)
        elif c == "=":
            self.addToken(tokenType.EQUAL_EQUAL if self.match('=') else tokenType.EQUAL)
        elif c == "<":
            self.addToken(tokenType.LESS_EQUAL if self.match("=") else tokenType.LESS)
        elif c == ">":
            self.addToken(tokenType.GREATER_EQUAL if self.match("=") else tokenType.GREATER)
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.isAtEnd():
                    self.advance()
            elif self.match("*"):
                self.multiLineComment()
            else:
                self.addToken(tokenType.SLASH)
        elif c == "o":
            if self.match('r'):
                self.addToken(tokenType.OR)
        elif c == "\"":
            self.string()
        elif c == "\t":
            pass
        elif c == "\n":
            self.line += 1
        elif c == " ":
            pass
        elif c == "\r":
            pass
        else:
            if self.isDigit(c):
                self.number()
            elif self.isAlpha(c):
                self.identifier()
            else:
                Error.error(self.line, "Unexpected character.")

    def multiLineComment(self):
        while self.peek() != "*" and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.isAtEnd() or self.peekNext() != "/":
            Error.error(self.line, "Comment block is not closed")
        self.advance()
        self.advance()
        if not self.isAtEnd():
            Error.error(self.line, "Wrong syntex")

    def isAlpha(self, c) -> bool:
         return (c >= 'a' and c <= 'z') or  (c >= 'A' and c <= 'Z') or c == '_'

    def isAlphaNumeric(self, c) -> bool:
        return self.isAlpha(c) or self.isDigit(c)

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text: str = self.source[self.start: self.current]
        if text in Scanner.keywords:
            type = Scanner.keywords[text]
        else:
            type = tokenType.IDENTIFIER
        self.addToken(type)
        
    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c 

    def addToken(self, tokenType: tokenType) -> None:
        self.addTokenHelper(tokenType, None)

    def addTokenHelper(self, type: tokenType, literal: object) -> None:
        text: str = self.source[self.start: self.current]
        self.tokens.append(Token(type, text, literal, self.line))


    def match(self, expected) -> bool: 
        if(self.isAtEnd()):
            return False
        if self.source[self.current] != expected:
            return False    
        self.current +=1 
        return True

    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.isAtEnd():
            Error.error(self.line, "Unterminated string")
            return 

        self.advance()

        value: str = self.source[self.start+1: self.current - 1]
        self.addTokenHelper(tokenType.STRING, value)

    def isDigit(self, c) -> bool:
        return c >= '0' and c <= '9'

    def peekNext(self):
        if self.current + 1 >=  len(self.source):
            return '\0' 
        return self.source[self.current + 1]

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()

        self.addTokenHelper(tokenType.NUMBER, float(self.source[self.start: self.current]) )


