from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.base import Base




class LogOfAch(Base):
    __tablename__ = 'logofach'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ach_id: Mapped[int] = mapped_column(Integer, ForeignKey('achievements.id'), nullable=False)
    achievement: Mapped[list['Achievements']] = relationship('Achievements', back_populates='log')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user: Mapped[list['User']] = relationship('User', back_populates='log')