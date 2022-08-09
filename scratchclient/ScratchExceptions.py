class ScratchExceptions(Exception):
    pass


class InvalidCredentialsException(ScratchExceptions):
    pass


class UnauthorizedException(ScratchExceptions):
    pass


class RejectedException(ScratchExceptions):
    pass


class CloudVariableException(ScratchExceptions):
    pass
