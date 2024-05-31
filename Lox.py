import sys
from Scanner import Scanner
from Parser import Parser
from Expr import Expr
from AstPrinter import AstPrinter
from RunTimeException import RunTimeException
from Interpreter import Interpreter

class Lox:
    hadError: bool = False
    hadRuntimeError: bool = False
    interpreter: Interpreter = Interpreter()

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        expression: Expr | None = parser.parse()
        if Lox.hadError:
            return
        #print(AstPrinter().print(expression))
        Lox.interpreter.interpret(expression)

    @staticmethod
    def runFile(path: str) -> None:
        inFile = open(path, 'rb') 
        bytes = inFile.read()
        inFile.close()
        # run the program
        if(Lox.hadError):
            return sys.exit(65)
        if(Lox.hadRuntimeError):
            return sys.exit(70)
        

    @staticmethod
    def runPrompt() -> None:
        while True:
            line = input("> ")
            if line is None:
                break
            Lox.run(line)
            Lox.hadError = False

    @staticmethod
    def runtimeError(error: RunTimeException):
        print(error.getMessage() + "\n[line " + error.token.line + "]")
        lox.hadRuntimeError = True

    def __init__(self, args: list[str]) -> None:
        if len(args) > 1:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(args) == 1:
            Lox.runFile(args[0])
        else:
            Lox.runPrompt()

lox = Lox([])
 