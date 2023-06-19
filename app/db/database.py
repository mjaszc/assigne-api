from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

env = os.environ["APPLICATION_ENV"]

if env == "testing":
    engine = create_engine(os.environ["TEST_DATABASE_URL"])
else:
    engine = create_engine(os.environ["DATABASE_URL"])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
