from sqlalchemy import ForeignKey
from extensions import db
from sqlalchemy.sql import func
from .user import User

class Report(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement = True)
  title = db.Column(db.String(255))
  owner = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
  date = db.Column(db.DateTime(timezone=True), server_default=func.now())
  
  content = db.Column(db.Text)