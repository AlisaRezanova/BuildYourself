import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import User
from models.exceptions import UserNotFoundError


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_user_id_by_tg_id(tg_id: int) -> int:
    with Session() as session:
        user = session.query(User).filter(User.tg_id == tg_id).first()
        if not user:
            raise UserNotFoundError
        user_id = user.id
        return user_id


def get_tg_id_by_id(us_id: int) -> int:
    with Session() as session:
        user = session.query(User).filter(User.id==us_id).first()
        if not user:
            raise UserNotFoundError
        return user.tg_id
