from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.base import Base



class Achievements(Base):
    __tablename__ = 'achievements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    img: Mapped[str] = mapped_column(String(250), nullable=True)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    log: Mapped[list['LogOfAch']] = relationship('LogOfAch', back_populates='achievement')