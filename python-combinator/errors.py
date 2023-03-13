class CompilerPanic(Exception):
    """An internal fatal error from which the compiler cannot safely recover"""

    def __init__(self, msg, content):
        super().__init__(f"{msg}: {content}")


class SemanticError(Exception):
    def __init__(self, msg, content):
        super().__init__(f"{msg}: {content}")
