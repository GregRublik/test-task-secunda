


class ModelAlreadyExistsException(BaseException):
    pass


class ModelNoFoundException(BaseException):
    pass

class ActivityValidationError(Exception):
    """Исключение для валидации активности"""
    pass