from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.database import Base


project_user_table = Table(
    "project_user",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    start_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    assigned_users = relationship("User", secondary=project_user_table, back_populates="assigned_projects")
