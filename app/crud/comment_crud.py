from sqlalchemy.orm import Session
import datetime

import app.schemas.project_schema as project_schema
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