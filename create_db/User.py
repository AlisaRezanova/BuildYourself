from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date
from db.base import Base



class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] =  mapped_column(Integer, primary_key=True)
    gender: Mapped[str] = mapped_column(String(2), nullable=False)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_of_reg: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    num_friends: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    habit: Mapped[list["Habits"]] = relationship("Habits", back_populates='user')
    fr1: Mapped[list['Friends']] = relationship('Friends', back_populates='user1', foreign_keys='Friends.fr1_id')
    fr2: Mapped[list['Friends']] = relationship('Friends', back_populates='user2', foreign_keys='Friends.fr2_id')
    log: Mapped[list['LogOfAch']] = relationship('LogOfAch', back_populates='user')
