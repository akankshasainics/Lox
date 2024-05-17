import sys

class Lox:
    hadError: bool = False
    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        for token in tokens:
            print(token)

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

    
    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print("[line {line}] Error {where} : {message}".format(line = line, where = where, message  = message))

    @staticmethod
    def error(line: int, message: str) -> None:
        Lox.report(line, "", message)


    def __init__(self, args: list[str]) -> None:
        if len(args) > 1:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(args) == 1:
            Lox.runFile(args[0])
        else:
            Lox.runPrompt()

 