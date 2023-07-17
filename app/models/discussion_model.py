from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Discussion(Base):
    __tablename__ = 'discussions'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    created_at = Column(Date)

    tasks = relationship("Task", back_populates="discussions")