"""Security"""


def user_has_permission(user, roles, data=None):
    """Permissions check against the user

    Checks the user's roles & associations to Youth, Units, etc. to
    determine whether they have the required authorization to perform
    the requested action.
    """
    # TO-DO: add unit tests for this
    if roles is str:
        roles = [roles]
    if 'Council.Admin' in user.roles:
        # Council admins can do ANYTHING!
        permission = True
    elif 'Council.Employee' in roles and 'Council.Employee' in user.roles:
        permission = True
    elif 'SponsoringOrganization.Admin' in roles and 'SponsoringOrganization.Admin' in user.roles:
        permission = user_has_sponsoring_organization_permission(user, data)
    elif 'Unit.Admin' in roles and 'Unit.Admin' in user.roles:
        permission = user_has_unit_permission(user, data)
    elif 'Guardian' in roles and 'Guardian' in user.roles:
        permission = user_has_guardian_permission(user, data)
    else:
        permission = False
    return permission


def user_has_sponsoring_organization_permission(user, data):  # pylint: disable=invalid-name
    """Determines whether the user has access to the sponsoring organization"""
    # TO-DO: implement this
    if user and data:
        return True


def user_has_unit_permission(user, data):
    """Determines whether the user has access to the unit"""
    # TO-DO: implement this
    if user and data:
        return True


def user_has_guardian_permission(user, data):
    """Determines whether the user has access to the youth"""
    # TO-DO: implement this
    if user and data:
        return True


def require_role(role):
    """Decorator function to require the user to have a specific role to perform an action"""
    def wrap(func):  # pylint: disable=missing-docstring
        def inner(*args, **kwargs):  # pylint: disable=missing-docstring
            if user_has_permission(args[0].user, role):
                return func(*args, **kwargs)
            else:
                # raise InsufficientPermissionException("You don't have authorization to perform the specified action.")
                raise InsufficientPermissionException(
                    "You don't have authorization ({}) to perform the specified action ({}).".
                    format(role, func.__name__)
                )
        return inner
    return wrap


class InsufficientPermissionException(Exception):
    """No unauthorized access for you!"""
    pass
