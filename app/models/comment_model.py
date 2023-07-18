from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DiscussionComment(Base):
    __tablename__ = 'discussion_comments'

    id = Column(Integer, primary_key=True, index=True)
    discussion_id = Column(Integer, ForeignKey('discussions.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String)
    created_at = Column(Date)

    discussion = relationship("Discussion", back_populates="comments")