from sqlalchemy.orm import Session
import datetime

import app.schemas.user_schema as user_schema
import app.schemas.comment_schema as comment_schema
import app.models.discussion_model as discussion_model
import app.schemas.discussion_schema as discussion_schema

def create_comment(db: Session, discussion: discussion_schema.Discussion, comment: comment_schema.CommentCreate, user: user_schema.User):
    new_comment = discussion_model.DiscussionComment(
        discussion_id = discussion,
        user_id=user.id,
        message=comment.message,
        created_at=datetime.date.today()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

def get_comment(db: Session, comment_id: int):
    return (
        db.query(discussion_model.DiscussionComment)
        .filter(discussion_model.DiscussionComment.id == comment_id)
        .first()
    )

def update_comment(db: Session, comment: comment_schema.Comment, comment_id: int, user_id: int):
    db_comment = db.query(discussion_model.DiscussionComment).filter(discussion_model.DiscussionComment.id == comment_id).first()
    if not db_comment:
        return None
    for key, value in comment.dict(exclude_unset=True).items():
        setattr(db_comment, key, value)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(discussion_model.DiscussionComment).filter(discussion_model.DiscussionComment.id == comment_id).first()
    if not db_comment:
        return False
    db.delete(db_comment)
    db.commit()
    return True