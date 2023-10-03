from sqlalchemy import ForeignKey
from extensions import db
from sqlalchemy.sql import func
from .question_group import QuestionGroup

class Question(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement = True)
  question = db.Column(db.String(255), nullable=False)
  answer = db.Column(db.String(100))
  question_group_id = db.Column(db.Integer, ForeignKey("question_group.id", ondelete='CASCADE'))
  code = db.Column(db.Text)
  
  @property
  def formatted_id(self):
    if self.question_group_id is not None:
      return f"{self.question_group_id}_{self.id}"
    else:
      return str(self.id)