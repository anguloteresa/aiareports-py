from flask import Flask, request, jsonify
from flask_restful import marshal_with, fields, marshal
from werkzeug.security import generate_password_hash
from extensions import db
from models.user import User
from .questionController import QuestionGroupModel

UserModel = {
  "id": fields.Integer,
  "first_name": fields.String,
  "last_name": fields.String,
  "email": fields.String,
  "password": fields.String,
  "bio": fields.String,
  "question_groups": fields.List(fields.Nested(QuestionGroupModel)),
}

@marshal_with(UserModel)
def getUsers():
  users = User.query.all()
  return users

def getUserByEmail():
  data = request.json
  email = data.get("email", None)
  user = User.query.filter_by(email = email).first()
  
  if user is None:
    return {"error": "Usuario no encontrado"}, 404
  
  return marshal(user, UserModel)

def getUserQuestions():
  # data = request.json
  # email = data.get("email", None)
  email = request.args.get("email")

  if email is None:
    return {"error": "Correo no proporcionado"}, 400

  user = User.query.filter_by(email = email).first()
  
  if user is None:
    return {"error": "Usuario no encontrado"}, 404

  user_groups = user.question_groups
  return marshal(user_groups, QuestionGroupModel)

@marshal_with(UserModel)
def getUser(user_id): 
  user = User.query.get_or_404(user_id)
  if user:
    return user
  return {"error": "Usuario no encontrado"}, 404

def userLogin():
  data = request.json
  email = data.get("email", None)
  password = data.get("password", None)
  
  if email is None:
    return {"message": "Correo de usuario no ingresado"}, 400
  
  if password is None:
    return {"message": "Contraseña no ingresada"}, 400
  
  existing_user = User.query.filter_by(email=email).first()
  
  if existing_user is None:
    return {"error": "Usuario no encontrado"}, 404
  
  if existing_user.check_password(password):
    return marshal(existing_user, UserModel)
  
  return {"error": "Contraseña incorrecta"}, 401

def createUser():
  if request.method == 'POST':
    data = request.json
    email = data.get("email", None)
    password = data.get("password", None)
    
    # Verificar si todos los campos requeridos están presentes
    if email is None or password is None:
      return {"error": "Faltan campos requeridos (email, password)"}, 400
    
    # Verificar si el usuario no existe ya
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
      return {"error": "El correo ya se encuentra en uso."}, 409
    
    # Encriptar la contraseña para añadir a la base de datos
    hashed = generate_password_hash(password)
    
    # Crear nombre desde correo
    name = email.split('@')[0].split('.')
    first_name = name[0].capitalize()
    last_name = name[1].capitalize()
    
    # Crear objeto de usuario y agregarlo a la base de datos
    user = User(first_name=first_name, last_name=last_name, email=email, password=hashed)
    db.session.add(user)
    db.session.commit()
    return marshal(user, UserModel)
  
  return {"error": "Método no permitido"}, 405  # Ejemplo: Devuelve un mensaje de error y un código 405 para otros métodos HTTP

@marshal_with(UserModel)
def deleteUser(user_id):
  if request.method == 'DELETE':
    user = User.query.get(user_id)
    if user is None:
      return {"error": "Usuario no encontrado."}, 404
    
    db.session.delete(user)
    db.session.commit()
    
    return {"message": "Usuario eliminado."} # Ejemplo: Devuelve un mensaje de error y un código 405 para otros métodos HTTP
  return {"error": "Método no permitido"}, 405

@marshal_with(UserModel)
def editUser(user_id):
  if request.method == 'POST':
    user = User.query.filter_by(id=user_id).first()
    if user is None:
      return {"error": "Usuario no encontrado."}, 404
    
    data = request.json
    
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.bio = data.get("bio", user.bio)
    
    db.session.merge(user)
    db.session.commit()
    return user
  
  return {"error": "Método no permitido"}, 405  # Ejemplo: Devuelve un mensaje de error y un código 405 para otros métodos HTTP
