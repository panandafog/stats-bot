import datetime

from models import User, Session, ActiveSession


class UserInfo:
    user = None
    total_time = None
    is_active = False

    @staticmethod
    def from_user(user: User, sessions: [Session], active_session: ActiveSession, start_datetime: datetime):
        user_info = UserInfo()
        user_info.user = user
        user_info.total_time = datetime.timedelta()

        for session in sessions:
            delta = datetime.timedelta()

            if session.end_time > start_datetime:
                if session.start_time > start_datetime:
                    delta = session.end_time - session.start_time
                else:
                    delta = session.end_time - start_datetime

            user_info.total_time += delta

        if active_session is not None:
            user_info.is_active = True

            delta = datetime.datetime.utcnow() - active_session.start_time
            user_info.total_time += delta

        return user_info


class TopUsers:
    users_info = []
    start_datetime = None
    first_entry = None
