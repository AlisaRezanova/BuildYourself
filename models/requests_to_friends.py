import os
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from models.create_db import Friends
from models.exceptions import FriendsNotAdded, FriendsNotFoundError
from datetime import date
from models.requests_to_users import get_user_id_by_tg_id


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_all_friends_by_user_id(tg_id: int) -> list:
    with Session() as session:
        user_id = get_user_id_by_tg_id(tg_id)
        friends = session.query(Friends).filter(or_(Friends.fr1_id==user_id, Friends.fr2_id==user_id)).all()
        friends = list(set(friends))
        return friends


def add_note_friends(tg_id: int, invite_code: str) -> bool:
    with Session() as session:
        user_id = get_user_id_by_tg_id(tg_id)
        new_friends = Friends(
            invite_code=invite_code,
            fr1_id = user_id
        )
        try:
            session.add(new_friends)
            session.commit()
            return True
        except Exception:
            raise FriendsNotAdded('friends not added')


def update_friends2(tg_id: int, invite_code) -> bool:
    with Session() as session:
        user_id = get_user_id_by_tg_id(tg_id)
        friends = session.query(Friends).filter(and_(Friends.invite_code == invite_code, Friends.fr2_id.is_(None))).first()
        if friends:
            friends.fr2_id = user_id
            friends.start_friendship = date.today()
            session.commit()
            return True
        else:
            return False



def check_eq_invite_code(invite_code: str):
    from handlers.friends import generate_invite_code
    with Session() as session:
        friends = session.query(Friends).all()
        codes = [fr.invite_code for fr in friends]
        if invite_code in codes:
            generate_invite_code()
        else:
            return invite_code


def update_fr_status(status: str, tg_id: int, fr_id: int) -> bool:
    with Session() as session:
        user_id = get_user_id_by_tg_id(tg_id)

        friend = session.query(Friends).filter(Friends.id == fr_id).first()
        if friend:
            friend.status = status
            session.commit()
            return True
        else:
            return False


def get_all_requests(tg_id: int) -> list:
    with Session() as session:
        user_id = get_user_id_by_tg_id(tg_id)
        requests = session.query(Friends).filter(Friends.fr1_id == user_id).filter(Friends.status == 'Waiting').filter(Friends.fr2_id != None).all()
        if requests:
            return requests
        else:
            raise FriendsNotFoundError('Friends Not Found Error')



