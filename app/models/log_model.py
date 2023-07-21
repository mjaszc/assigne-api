from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String, index=True)
    details = Column(String)