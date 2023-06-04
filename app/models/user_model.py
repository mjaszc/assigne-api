from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship
from app.models.project_model import project_user_table

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="author")
    assigned_projects = relationship("Project", secondary=project_user_table, back_populates="assigned_users")

    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.password)
