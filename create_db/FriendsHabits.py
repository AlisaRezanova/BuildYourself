from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.base import Base



class FriendsHabits(Base):
    __tablename__ = 'friendshabits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    friend_id: Mapped[int] = mapped_column(Integer, ForeignKey('friends.id'), nullable=False)
    habit_id: Mapped[int] = mapped_column(Integer, ForeignKey('habits.id'), nullable=False)
    status: Mapped[str] = mapped_column(String(25), nullable=False, default='waiting_habit')
    receiver_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, nullable=False)

    friends: Mapped[list['Friends']] = relationship('Friends',  back_populates='frhab')
    habits: Mapped[list['Habits']] = relationship('Habits', back_populates='frhab')
