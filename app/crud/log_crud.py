from sqlalchemy.orm import Session
import app.models.log_model as log_model 

def create_log(db: Session, action: str, details: str):
    db_log = log_model.Log(action=action, details=details)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log