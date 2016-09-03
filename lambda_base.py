"""Default Lambda functions"""
from models import Session


def get_session(event):
    """Get the session from the event

    Session will be created if it doesn't exist.
    """
    if 'session_uuid' in event:
        session = Session.Factory().load_by_uuid(event['session_uuid'])
    else:
        session = Session.Session()
    return session
