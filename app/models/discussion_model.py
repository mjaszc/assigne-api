from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Discussion(Base):
    __tablename__ = 'discussions'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    created_at = Column(Date)

    comments = relationship("DiscussionComment", back_populates="discussion")

class DiscussionComment(Base):
    __tablename__ = 'discussion_comments'

    id = Column(Integer, primary_key=True, index=True)
    discussion_id = Column(Integer, ForeignKey('discussions.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String)
    created_at = Column(Date)

    discussion = relationship("Discussion", back_populates="comments")