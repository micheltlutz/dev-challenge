from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
basedir = os.path.abspath(os.path.dirname(__file__))


DATABASE_URL = "sqlite:///./dev-challenge.db"

engine = create_engine(DATABASE_URL, echo=True)
with engine.connect() as conn:
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

