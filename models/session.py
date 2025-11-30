from sqlalchemy.orm import sessionmaker
from create_db.create_db import engine

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
