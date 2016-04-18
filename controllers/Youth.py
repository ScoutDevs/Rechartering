# pylint: disable=import-error
"""Youth Controller"""

from controllers import InvalidActionException
from controllers.Security import require_role
from models import Youth


class Controller(object):
    """Youth Controller"""

    def __init__(self,
                 user,
                 youth_factory=Youth.YouthFactory(),
                 youth_persister=Youth.YouthPersister()):
        """Dependency-injectable init

        Args:
            user: User object, used to determine permissions
            youth_factory: Youth factory object
            youth_persister: Youth persister object
        """
        self.user = user
        self.youth_factory = youth_factory
        self.youth_persister = youth_persister

    @require_role(['Unit.Admin', 'Guardian', 'SponsoringOrganization.Admin', 'Council.Employee'])
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
        youth = self.youth_factory.construct(youth_data)
        duplicates = self.youth_persister.find_potential_duplicates(youth)
        return duplicates

    @require_role('Guardian')
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

    @require_role('Guardian')
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
        if guardian.id == youth.guardian_approval_guardian_id:
            youth.guardian_approval_guardian_id = ''
            youth.guardian_approval_signature = ''
            youth.guardian_approval_date = ''
            return youth
        else:
            raise InvalidActionException('Only the guardian who granted approval can revoke it.')
