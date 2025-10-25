import os
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from models.create_db import User


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def deeleetee():
    with Session() as session:
        stmt = (delete(User).where(User.id == 2))
        session.execute(
            stmt)
        session.commit()
        all_users = session.query(User).all()
        for user in all_users:
            print(user.id, user.sex, user.tg_id, user.date_of_reg, user.num_friends)


def show():
    with Session() as session:
        current_user = session.query(User).filter(User.tg_id == 000).first()
        print(current_user)

deeleetee()
