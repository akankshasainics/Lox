import sys
from Scanner import Scanner
from Parser import Parser
from Expr import Expr
from Stmt import Stmt
from AstPrinter import AstPrinter
from RunTimeException import RunTimeException
from Interpreter import Interpreter


"""
1. Lox class -> Lox instance
2. Visitor(Lox)
3.  @dataclass
"""


# Singletone
class Lox:
    def __init__(self):
        self.hadError: bool = False
        self.hadRuntimeError: bool = False
        self.interpreter: Interpreter = Interpreter()

    def setError(self):
        self.hadError = True

    def run(self,source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements: list[Stmt] = parser.parse()
        if self.hadError:
            return
        self.interpreter.interpret(statements)

    def runFile(self, path: str) -> None:
        inFile = open(path, 'rb') 
        bytes = inFile.read()
        inFile.close()
        source = bytes.decode("utf-8")
        self.run(source)
        # run the program
        if(self.hadError):
            return sys.exit(65)
        if(self.hadRuntimeError):
            return sys.exit(70)
    
    def runPrompt(self) -> None:
        while True:
            line = input("> ")
            if line is None:
                break
            self.run(line)
            self.hadError = False

    def runtimeError(self, error: RunTimeException):
        print(error.getMessage() + "\n[line " + str(error.token.line) + "]")
        self.hadRuntimeError = True

    def runFromArgs(self, args):
        if len(args) > 1:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(args) == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()
        
        
LOX = Lox()

if __name__ == "__main__":
    LOX.runFromArgs(sys.argv[1:])
