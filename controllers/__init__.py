"""
Here be controllers

Controllers should support dependency injection and should be able to be tested
completely free of DB & network dependencies.
"""


def require_status(status):
    """Decorator for application functions"""
    def wrap(func):  # pylint: disable=missing-docstring
        def inner(*args, **kwargs):  # pylint: disable=missing-docstring
            app = args[1]
            if app.status != status:
                raise InvalidActionException(
                    'Can only submit guardian approval for applications in "{}" status; current status: "{}"'.
                    format(
                        status,
                        app.status,
                    )
                )
            return func(*args, **kwargs)
        return inner
    return wrap


class InvalidActionException(Exception):
    """The action attempted is not valid"""
    pass
