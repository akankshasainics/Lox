
class Error:
    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print("[line {line}] Error {where} : {message}".format(line = line, where = where, message  = message))

    @staticmethod
    def error(line: int, message: str) -> None:
        Error.report(line, "", message)