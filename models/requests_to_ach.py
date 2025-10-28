import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import Achievements, LogOfAch
from models.exceptions import AchNotFoundError
from models.requests_to_users import get_user_id_by_tg_id


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_description_about_ach(ach_id: int):
    with Session() as session:
        ach = session.query(Achievements).filter(Achievements.id == ach_id).first()
        img = ach.img
        description = ach.description
        return img, description