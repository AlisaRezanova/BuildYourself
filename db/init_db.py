from base import Base, engine
from create_db import User, Achievements, Friends, FriendsHabits, Habits, LogOfHabits, LogOfAch

def init_db():
    Base.metadata.create_all(bind=engine)