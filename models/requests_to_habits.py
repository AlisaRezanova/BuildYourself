import os
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from models.create_db import User, Habits, LogOfHabits
from .exceptions import UserNotFoundError, LogNotFoundError
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta
from io import BytesIO


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_all_habits_by_user_id(tg_id: int) -> list:
    with Session() as session:
        user_id = session.query(User).filter(User.tg_id==tg_id).first().id
        if not user_id:
            raise UserNotFoundError()
        all_habits = session.query(Habits).filter(Habits.user_id==user_id).all()
        return all_habits


def get_progress_by_week(hab_id: int):
    with Session() as session:
        log_entries = session.query(LogOfHabits).filter_by(habit_id=hab_id).all()
        if not log_entries:
            raise LogNotFoundError("Нет данных по привычке")
        df = pd.DataFrame({
            'date': [entry.date_of_mark for entry in log_entries],
            'completed': 1
        })
        df.set_index('date', inplace=True)
        full_index = pd.date_range(start=date.today()-timedelta(days=6), end=date.today(), freq='D')
        df = df.reindex(full_index, fill_value=0)
        df.index.name = 'date'
        weekly_progress = df['completed'].resample('D').mean() * 100
        weekly_progress.index = weekly_progress.index.date
        plt.figure()
        weekly_progress.plot(kind='bar')
        plt.xlabel('Неделя')
        plt.ylabel('Процент выполнения')
        plt.title('Прогресс привычки за неделю')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf


def get_progress_by_month(hab_id: int):
    ...

def get_progress_by_half_year(hab_id: int):
    ...

def get_progress_by_year(hab_id: int):
    ...
