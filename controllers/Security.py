"""Security"""

ROLE_COUNCIL_ADMIN = 'Council.Admin'
ROLE_COUNCIL_EMPLOYEE = 'Council.Employee'
ROLE_SPORG_ADMIN = 'SponsoringOrganization.Admin'
ROLE_UNIT_ADMIN = 'Unit.Admin'
ROLE_GUARDIAN = 'Guardian'


def user_has_permission(user, roles):
    """Permissions check against the user

    Checks the user's roles & associations to Youth, Units, etc. to
    determine whether they have the required authorization to perform
    the requested action.
    """
    # TO-DO: add unit tests for this
    if roles is str:
        roles = [roles]
    if ROLE_COUNCIL_ADMIN in user.roles:
        # Council admins can do ANYTHING!
        permission = True
    elif ROLE_COUNCIL_EMPLOYEE in roles and ROLE_COUNCIL_EMPLOYEE in user.roles:
        permission = True
    elif ROLE_SPORG_ADMIN in roles and ROLE_SPORG_ADMIN in user.roles:
        permission = True
    elif ROLE_UNIT_ADMIN in roles and ROLE_UNIT_ADMIN in user.roles:
        permission = True
    elif ROLE_GUARDIAN in roles and ROLE_GUARDIAN in user.roles:
        permission = True
    else:
        permission = False
    return permission


def user_has_sponsoring_organization_permission(user, *args):  # pylint: disable=invalid-name
    """Determines whether the user has access to the sponsoring organization"""
    # TO-DO: implement this
    if user and args:
        return True


def user_has_unit_permission(user, *args):
    """Determines whether the user has access to the unit"""
    # TO-DO: implement this
    if user and args:
        return True


def user_has_guardian_permission(user, *args):
    """Determines whether the user has access to the youth"""
    # TO-DO: implement this
    print args
    if user and args:
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
