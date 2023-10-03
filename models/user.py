from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement = True)
  first_name = db.Column(db.String(100))
  last_name = db.Column(db.String(100))
  email = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)  # Almacenar el hash de la contraseña
  bio = db.Column(db.Text)
  
  question_groups = db.relationship('QuestionGroup', cascade="delete", backref='user', lazy=True)
  
  def set_password(self, password):
    # Genera el hash de la contraseña y almacénalo en la columna password_hash
    self.password = generate_password_hash(password)
  
  def check_password(self, password):
    # Comprueba si la contraseña proporcionada coincide con el hash almacenado
    return check_password_hash(self.password, password)