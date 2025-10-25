import os
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from models.create_db import User, Habits

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


def filling_habits():
    with Session() as session:
        hab1 = Habits(
            user_id = 1,
            name = 'Бег по утрам'
        )

        hab2 = Habits(
            user_id=1,
            name='Бег по вечерам'
        )

        hab3 = Habits(
            user_id=1,
            name='Не есть сладкое'
        )

        session.add_all([hab1, hab2, hab3])
        session.commit()

        all_habits = session.query(Habits).all()
        for habit in all_habits:
            print(habit.id, habit.user_id, habit.name)

filling_habits()
