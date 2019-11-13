class InsufficientFunds(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class InvalidPermissions(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
