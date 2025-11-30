from sqlalchemy import Integer, String, ForeignKey, Date
from datetime import date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.base import Base



class Friends(Base):
    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invite_code: Mapped[str] = mapped_column(String(10), nullable=False)
    fr1_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    fr2_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(100), default='Waiting', nullable=False)
    start_friendship: Mapped[date] = mapped_column(Date, nullable=True)

    user1: Mapped[list['User']] = relationship('User', back_populates='fr1', foreign_keys=[fr1_id])
    user2: Mapped[list['User']] = relationship('User', back_populates='fr2', foreign_keys=[fr2_id])
    frhab: Mapped[list['FriendsHabits']] = relationship('FriendsHabits', back_populates='friends')