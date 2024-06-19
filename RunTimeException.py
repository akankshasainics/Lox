from Token import Token

class RunTimeException(Exception):
    def __init__(self, token: Token, message) -> None:
        super().__init__(message)
        self.message = message
        self.token = token

    def getMessage(self):
        return self.message
    