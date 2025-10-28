import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import LogOfHabits
from .exceptions import LogNotFoundError
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta
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