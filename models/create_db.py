from collections import defaultdict
from datetime import datetime, date
from sqlalchemy import create_engine, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship


engine = create_engine('sqlite:///buildyourself.db')

Base = declarative_base()

#Base.metadata.drop_all(engine)

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] =  mapped_column(Integer, primary_key=True)
    sex: Mapped[str] = mapped_column(String(2), nullable=False)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_of_reg: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    num_friends: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    habit: Mapped[list["Habits"]] = relationship("Habits", back_populates='user')
    fr1: Mapped[list['Friends']] = relationship('Friends', back_populates='user1', foreign_keys='Friends.fr1_id')
    fr2: Mapped[list['Friends']] = relationship('Friends', back_populates='user2', foreign_keys='Friends.fr2_id')
    log: Mapped[list['LogOfAch']] = relationship('LogOfAch', back_populates='user')


class Habits(Base):
    __tablename__ = 'habits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user: Mapped[list["User"]] = relationship("User", back_populates='habit')
    log: Mapped[list['LogOfHabits']] = relationship('LogOfHabits', back_populates='habit')
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    day_len: Mapped[int] = mapped_column(Integer, default=14, nullable=False)
    notification: Mapped[bool] = mapped_column(Boolean, default=1, nullable=False)


class LogOfHabits(Base):
    __tablename__ = 'logofhabits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    habit_id: Mapped[int] = mapped_column(Integer, ForeignKey('habits.id'), nullable=False)
    habit: Mapped[list['Habits']] = relationship('Habits', back_populates='log')
    date_of_mark: Mapped[date] = mapped_column(Date, nullable=False)


class Friends(Base):
    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fr1_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    fr2_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    status: Mapped[str] = mapped_column(String(100), default='Waiting', nullable=False)
    start_friendship: Mapped[date] = mapped_column(Date)
    user1: Mapped[list['User']] = relationship('User', back_populates='fr1', foreign_keys=[fr1_id])
    user2: Mapped[list['User']] = relationship('User', back_populates='fr2', foreign_keys=[fr2_id])


class Achievements(Base):
    __tablename__ = 'achievements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    img: Mapped[str] = mapped_column(String(250), nullable=True)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    log: Mapped[list['LogOfAch']] = relationship('LogOfAch', back_populates='achievement')


class LogOfAch(Base):
    __tablename__ = 'logofach'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ach_id: Mapped[int] = mapped_column(Integer, ForeignKey('achievements.id'), nullable=False)
    achievement: Mapped[list['Achievements']] = relationship('Achievements', back_populates='log')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user: Mapped[list['User']] = relationship('User', back_populates='log')

Base.metadata.create_all(engine)
