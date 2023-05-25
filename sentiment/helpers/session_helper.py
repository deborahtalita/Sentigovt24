from accounts.models import Session

def isGuestLimitAccess(cookies):
    session_id = cookies['session_id']

    session = Session.objects.get(id=session_id)
    if session:
        if session.quota == 0:
            return True
        else:
            session.quota = session.quota - 1
            session.save()
    
    return False