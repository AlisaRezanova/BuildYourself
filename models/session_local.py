from sqlalchemy.orm import sessionmaker
from .create_db import engine


Session = sessionmaker(bind=engine)
session = Session()