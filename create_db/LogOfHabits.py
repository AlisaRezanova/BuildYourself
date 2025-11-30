from sqlalchemy import Integer, ForeignKey, Date
from datetime import date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.base import Base



class LogOfHabits(Base):
    __tablename__ = 'logofhabits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    habit_id: Mapped[int] = mapped_column(Integer, ForeignKey('habits.id'), nullable=False)
    habit: Mapped[list['Habits']] = relationship('Habits', back_populates='log')
    date_of_mark: Mapped[date] = mapped_column(Date, nullable=False)