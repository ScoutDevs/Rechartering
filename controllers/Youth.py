# pylint: disable=import-error
"""Youth Controller"""

from controllers import ClientErrorException
from controllers import InvalidActionException
from controllers import Security
from controllers.Security import require_role
from models import Youth


class Controller(object):
    """Youth Controller"""

    def __init__(self,
                 user,
                 factory=None):
        """Dependency-injectable init

        Args:
            user: User object, used to determine permissions
            factory: Youth factory object
        """
        self.user = user

        if factory:
            self.factory = factory
        else:
            self.factory = Youth.YouthFactory()

        self.persister = self.factory.get_persister()

    @require_role([
        Security.ROLE_COUNCIL_ADMIN,
        Security.ROLE_COUNCIL_EMPLOYEE,
        Security.ROLE_UNIT_ADMIN,
        Security.ROLE_SPORG_ADMIN,
        Security.ROLE_GUARDIAN
    ])
    def find_duplicate_youth(self, youth_data):
        # TO-DO: Do we need some sort of captcha to protect this data?
        """Search to see if the youth is already in the system

        Duplicate records for the same individual are to be avoided as much
        as possible. This will check for duplicate youth already in the
        system, allowing the user to submit an application using an existing
        record rather than creating new one.

        Args:
            youth_data: dict containing the data describing the Youth
        Returns:
            List of Youth records who are potential duplicates
        """
        youth = self.factory.construct(youth_data)
        duplicates = self.persister.find_potential_duplicates(youth)
        return duplicates

    @require_role(Security.ROLE_GUARDIAN)
    def grant_guardian_approval(self, youth, data):  # pylint: disable=no-self-use
        """Put guardian approval on file for their Youth

        When a guardian grants approval for a Youth to participate in the BSA,
        we keep it on file until revoked.

        Args:
            youth: Youth object
            data: dict containing approval data
        Returns:
            Youth object (updated)
        """
        youth.guardian_approval_guardian_id = data['guardian_approval_guardian_id']
        youth.guardian_approval_signature = data['guardian_approval_signature']
        youth.guardian_approval_date = data['guardian_approval_date']
        return youth

    @require_role(Security.ROLE_GUARDIAN)
    def revoke_guardian_approval(self, guardian, youth):  # pylint: disable=no-self-use
        """Revokes guardian approval for the specified Youth

        If a guardian wishes to revoke their approval for a youth, they have
        that option.

        Args:
            guardian: Guardian object representing the guardian revoking approval
            youth: Youth whose approval is being revoked
        Raises:
            InvalidActionException: when guardian doesn't match youth's approval
        Returns:
            Youth object (updated)
        """
        if guardian.uuid == youth.guardian_approval_guardian_id:
            youth.guardian_approval_guardian_id = ''
            youth.guardian_approval_signature = ''
            youth.guardian_approval_date = ''
            return youth
        else:
            raise InvalidActionException('Only the guardian who granted approval can revoke it.')

    @require_role([
        Security.ROLE_COUNCIL_ADMIN,
        Security.ROLE_COUNCIL_EMPLOYEE,
        Security.ROLE_UNIT_ADMIN,
        Security.ROLE_SPORG_ADMIN,
        Security.ROLE_GUARDIAN
    ])
    def get(self, uuid):
        """Get

        Args:
            uuid: string
        Returns:
            object
        """
        return self.factory.load_by_uuid(uuid)

    @require_role([
        Security.ROLE_COUNCIL_ADMIN,
        Security.ROLE_COUNCIL_EMPLOYEE,
        Security.ROLE_UNIT_ADMIN,
        Security.ROLE_SPORG_ADMIN,
        Security.ROLE_GUARDIAN
    ])
    def set(self, data):
        """Record-level create/update

        Args:
            data: dict containing the record data; will REPLACE any existing
                record in its entirety
        Returns:
            Updated object
        """
        obj = self.factory.construct(data)
        obj.validate()
        return obj

    @require_role([
        Security.ROLE_COUNCIL_ADMIN,
        Security.ROLE_COUNCIL_EMPLOYEE,
        Security.ROLE_UNIT_ADMIN,
        Security.ROLE_SPORG_ADMIN,
        Security.ROLE_GUARDIAN
    ])
    def update(self, data):
        """Field-level create/update

        Args:
            data: dict containing the data to update; will MODIFY any
                existing record
        Returns:
            Updated object
        """
        if 'uuid' in data and data['uuid']:
            obj = self.factory.load_by_uuid(data['uuid'])
            obj.set_from_data(data)
            obj.validate()
            return obj
        else:
            raise ClientErrorException('No uuid specified.')

    @require_role([Security.ROLE_COUNCIL_ADMIN, Security.ROLE_COUNCIL_EMPLOYEE])
    def search(self, search_data):
        """Find

        Args:
            search_data: dict containing data to search for
        Returns:
            list of dicts
        """
        return self.persister.query(search_data)
