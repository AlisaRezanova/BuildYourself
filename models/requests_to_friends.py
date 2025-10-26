import os
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from models.create_db import Friends, User
from models.exceptions import UserNotFoundError


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_all_friends_by_user_id(tg_id: int) -> list:
    with Session() as session:
        user_id = session.query(User).filter(User.tg_id == tg_id).first().id
        if not user_id:
            raise UserNotFoundError
        friends = session.query(Friends).filter(or_(Friends.fr1_id==user_id, Friends.fr2_id==user_id)).all()
        friends = list(set(friends))
        return friends


def get_tg_id_by_id(us_id: int) -> int:
    with Session() as session:
        user = session.query(User).filter(User.id==us_id).first()
        if not user:
            raise UserNotFoundError
        return user.tg_id