from sqlalchemy import ForeignKey
from extensions import db
from sqlalchemy.sql import func
from .user import User

class QuestionGroup(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement = True)
  name = db.Column(db.String(100), nullable=False)
  owner = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
  created_at = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())
  description = db.Column(db.Text)
  
  questions = db.relationship('Question', cascade="delete", backref='question_group', lazy=True)
