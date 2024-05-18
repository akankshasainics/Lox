import sys
from Scanner import Scanner

class Lox:
    hadError: bool = False
    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        for token in tokens:
            print(token.line, end=" ")
            print(token.lexeme, end= " ")
            print(token.literal, end= " ")
            print(token.type)
            print("------------------")

    @staticmethod
    def runFile(path: str) -> None:
        inFile = open(path, 'rb') 
        bytes = inFile.read()
        inFile.close()
        # run the program
        if(Lox.hadError):
            return sys.exit(65)
        

    @staticmethod
    def runPrompt() -> None:
        while True:
            line = input("> ")
            if line is None:
                break
            Lox.run(line)
            Lox.hadError = False


    def __init__(self, args: list[str]) -> None:
        if len(args) > 1:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(args) == 1:
            Lox.runFile(args[0])
        else:
            Lox.runPrompt()

lox = Lox([])
 