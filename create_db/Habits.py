from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.base import Base


class Habits(Base):
    __tablename__ = 'habits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user: Mapped[list["User"]] = relationship("User", back_populates='habit')
    log: Mapped[list['LogOfHabits']] = relationship('LogOfHabits', back_populates='habit')
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    day_len: Mapped[int] = mapped_column(Integer, default=14, nullable=False)
    notification: Mapped[bool] = mapped_column(Boolean, default=1, nullable=False)
    is_coop: Mapped[str] = mapped_column(String(3), nullable=False, default='no')

    frhab: Mapped[list["FriendsHabits"]] = relationship("FriendsHabits", back_populates='habits')