import datetime

from models import User, Session, ActiveSession

class UserInfo:
    user = None
    total_time = None
    is_active = False

    @staticmethod
    def from_user(user: User, sessions: [Session], active_session: ActiveSession):
        user_info = UserInfo()
        user_info.user = user
        user_info.total_time = datetime.timedelta()

        for session in sessions:
            delta = session.end_time - session.start_time
            user_info.total_time += delta

        if not active_session is None:
            user_info.is_active = True

            delta = datetime.datetime.utcnow() - active_session.start_time
            user_info.total_time += delta

        return user_info

class TopUsers:
    users_info = []
    start_datetime = None
