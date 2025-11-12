import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import LogOfHabits, Habits
from .exceptions import LogNotFoundError
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta, datetime
from io import BytesIO


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_progress_by_week(hab_id: int):
    with Session() as session:
        log_entries = session.query(LogOfHabits).filter_by(habit_id=hab_id).all()
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
        plt.figure(figsize=(12, 8))
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
    with Session() as session:
        log_entries = session.query(LogOfHabits).filter_by(habit_id=hab_id).all()
        df = pd.DataFrame({
            'date': [entry.date_of_mark for entry in log_entries],
            'completed': 1
        })
        df.set_index('date', inplace=True)
        full_index = pd.date_range(start=date.today() - timedelta(days=30), end=date.today(), freq='D')
        df = df.reindex(full_index, fill_value=0)
        df.index.name = 'date'
        monthly_progress = df['completed'].resample('W').mean() * 100
        monthly_progress.index = monthly_progress.index.date #Поменять индексы на нормальные обозначения (Либо неделя1, 2 и тд либо диапазон дат)
        plt.figure(figsize=(12, 8))
        monthly_progress.plot(kind='bar')
        plt.xlabel('Недели')
        plt.ylabel('Процент выполнения')
        plt.title('Прогресс привычки за месяц')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf


def get_progress_by_half_year(hab_id: int):
    with Session() as session:
        log_entries = session.query(LogOfHabits).filter_by(habit_id=hab_id).all()
        df = pd.DataFrame({
            'date': [entry.date_of_mark for entry in log_entries],
            'completed': 1
        })
        df.set_index('date', inplace=True)
        full_index = pd.date_range(start=date.today() - timedelta(days=181), end=date.today(), freq='D')
        df = df.reindex(full_index, fill_value=0)
        df.index.name = 'date'
        monthly_progress = df['completed'].resample('ME').mean() * 100
        monthly_progress.index = monthly_progress.index.date
        plt.figure(figsize=(12, 28))
        monthly_progress.plot(kind='bar')
        plt.xlabel('Месяц')
        plt.ylabel('Процент выполнения')
        plt.title('Прогресс привычки за полгода')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf

def get_progress_by_year(hab_id: int):
    with Session() as session:
        log_entries = session.query(LogOfHabits).filter_by(habit_id=hab_id).all()
        df = pd.DataFrame({
            'date': [entry.date_of_mark for entry in log_entries],
            'completed': 1
        })
        df.set_index('date', inplace=True)
        full_index = pd.date_range(start=date.today() - timedelta(days=365), end=date.today(), freq='D')
        df = df.reindex(full_index, fill_value=0)
        df.index.name = 'date'
        monthly_progress = df['completed'].resample('ME').mean() * 100
        monthly_progress.index = monthly_progress.index.date
        plt.figure(figsize=(12, 8))
        monthly_progress.plot(kind='bar')
        plt.xlabel('Месяц')
        plt.ylabel('Процент выполнения')
        plt.title('Прогресс привычки за полгода')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf

def mark_habit_today(habit_id: int) -> None:
    with Session() as session:
        existing_mark = session.query(LogOfHabits).filter(LogOfHabits.habit_id == habit_id, LogOfHabits.date_of_mark == date.today()).first()
        if existing_mark:
            raise ValueError("Привычка уже отмечена за сегодня")

        new_mark = LogOfHabits(habit_id=habit_id, date_of_mark=date.today())
        session.add(new_mark)
        session.commit()

def mark_habit_by_date(habit_id: int, mark_date: date) -> None:
    with Session() as session:
        existing_mark = session.query(LogOfHabits).filter(LogOfHabits.habit_id == habit_id,
                                                          LogOfHabits.date_of_mark == mark_date).first()
        if existing_mark:
            raise ValueError(f"Привычка уже отмечена за {mark_date}")

        new_mark = LogOfHabits(habit_id=habit_id, date_of_mark=mark_date)
        session.add(new_mark)
        session.commit()

def get_habits_marks(habit_id: int) -> list[LogOfHabits]:
    with Session() as session:
        marks = session.query(LogOfHabits).filter(LogOfHabits.habit_id == habit_id).all()
        return marks


def get_first_mark_date(habit_id: int) -> datetime:
    with Session() as session:
        first_mark = session.query(LogOfHabits).filter(
            LogOfHabits.habit_id == habit_id
        ).order_by(LogOfHabits.date_of_mark.asc()).first()

        if first_mark:
            return datetime.combine(first_mark.date_of_mark, datetime.min.time())
        return None

def get_habit_marks_count(habit_id: int) -> int:
    with Session() as session:
        count = session.query(LogOfHabits).filter(LogOfHabits.habit_id == habit_id).count()
        return count

def delete_habit(habit_id: int):
    with Session() as session:
        session.query(LogOfHabits).filter(LogOfHabits.habit_id == habit_id).delete()
        session.query(Habits).filter(Habits.id == habit_id).delete()
        session.commit()

