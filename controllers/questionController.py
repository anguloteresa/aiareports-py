from models.user import User
from models.question import Question
from models.question_group import QuestionGroup
from extensions import db
from flask import Flask, request, jsonify
from flask_restful import marshal_with, fields, marshal
from sqlalchemy.sql import func

QuestionModel = {
  "id": fields.Integer,
  "question": fields.String,
  "answer": fields.String,
  "question_group_id": fields.Integer,
  "code": fields.String,
}

QuestionGroupModel = {
  "id": fields.Integer,
  "name": fields.String,
  "owner": fields.Integer,
  "created_at": fields.DateTime,
  "description": fields.String,
  "questions": fields.List(fields.Nested(QuestionModel)),
}

UserModel = {
  "id": fields.Integer,
  "first_name": fields.String,
  "last_name": fields.String,
  "email": fields.String,
  "password": fields.String,
  "bio": fields.String,
  "question_groups": fields.List(fields.Nested(QuestionGroupModel)),
}

# CREATE
def createQuestionGroup():
  if request.method == 'POST':
    data = request.json
    name = data.get("name", None)
    owner = data.get("owner", None)
    description = data.get("description", None)
    
    if name is None or owner is None:
      return {"error": "Faltan campos requeridos (name, owner)"}, 400
    
    group = QuestionGroup(name = name, owner = owner, description = description)
    db.session.add(group)
    db.session.commit()
    
    return marshal(group, QuestionGroupModel)
  
  return {"error": "Método no permitido"}, 405  # Ejemplo: Devuelve un mensaje de error y un código 405 para otros métodos HTTP

def createTest():
  if request.method == 'POST':
    data = request.json
    question = data.get("question", None)
    answer = data.get("answer", None)
    question_group_id = data.get("question_group_id", None)
    code = data.get("code", None)
    
    if question is None:
      return {"error": "Faltan campos requeridos (question)"}, 400
    
    if question_group_id is None:
      return {"error": "Faltan campos requeridos (question_group_id)"}, 400
    
    group = QuestionGroup.query.get(question_group_id)
    
    if group is None:
      return {"error": "El grupo de preguntas " + question_group_id + " no existe."}, 404    
    
    question = Question(question = question, answer = answer, code = code, question_group_id = question_group_id)
    db.session.add(question)
    db.session.commit()
    return marshal(question, QuestionModel)
  return {"error": "Método no permitido"}, 405

def createQuestion(group_id):
  if request.method == 'POST':
    data = request.json
    question = data.get("question", None)
    answer = data.get("answer", None)
    question_group_id = data.get("question_group_id", None)
    code = data.get("code", None)
    
    if question is None:
      return {"error": "Faltan campos requeridos (question)"}, 400
    
    group = QuestionGroup.query.get(group_id)
    
    if group is None:
      return {"error": "El grupo de preguntas " + group_id + " no existe."}, 404    
    
    question = Question(question = question, answer = answer, code = code, question_group_id = group_id)
    db.session.add(question)
    db.session.commit()
    return marshal(question, QuestionModel)
  return {"error": "Método no permitido"}, 405

# READ
def getQuestions():
  if request.method == 'GET':
    questions = Question.query.all()
    print(questions)
    return marshal(questions, QuestionModel)
  
  return {"error": "Método no permitido"}, 405  


def getQuestionGroups():
  if request.method == 'GET':
    questions = QuestionGroup.query.all()
    return marshal(questions, QuestionGroupModel)
  
  return {"error": "Método no permitido"}, 405  

def getQuestionsInGroup(group_id):
  if request.method == 'GET':
    group = QuestionGroup.query.get(group_id)
    
    if group is None:
      return {"error": "El grupo de preguntas " + group_id + " no existe."}, 404
    
    questions_in_group = group.questions
    return marshal(questions_in_group, QuestionModel)
  
  return {"error": "Método no permitido"}, 405

def getQuestion(question_id):
  if request.method == 'GET':
    question = Question.query.get(question_id)
    
    if question is None:
      return {"error": "La pregunta " + question_id + " no existe."}, 404
    
    return marshal(question, QuestionModel)
  
  return {"error": "Método no permitido"}, 405  


# UPDATE
def editQuestionGroup(group_id):
  if request.method == 'POST':
    group = QuestionGroup.query.filter_by(id = group_id).first()
    
    if group is None:
      return {"error": "El grupo de preguntas " + group_id + " no existe."}, 404    
    
    data = request.json
    group.name = data.get("name", group.name)
    group.description = data.get("description", group.description)
    
    db.session.merge(group)
    db.session.commit()
    
    return group
  return {"error": "Método no permitido"}, 405

def editQuestion(question_id):
  if request.method == 'POST':
    question = Question.query.get(question_id)
    
    if question is None:
      return {"error": "La pregunta " + question_id + " no existe."}, 404
    
    data = request.json
    
    question.question = data.get("name", question.question)
    question.answer = data.get("description", question.answer)
    question.code = data.get("code", question.code)
    
    db.session.merge(question)
    db.session.commit()
    
    return marshal(question, QuestionModel)
  return {"error": "Método no permitido"}, 405 

# DELETE
def deleteQuestionGroup(group_id):
  if request.method == 'DELETE':
    group = QuestionGroup.query.filter_by(id = group_id).first()
    
    if group is None:
      return {"error": "El grupo de preguntas " + group_id + " no existe."}, 404
    
    db.session.delete(group)
    db.session.commit()
    return {"message": "Grupo de preguntas eliminado."}
  
  return {"error": "Método no permitido"}, 405

def deleteQuestion(question_id):
  if request.method == 'DELETE':
    question = Question.query.get(question_id)
    
    if question is None:
      return {"error": "La pregunta " + question_id + " no existe."}, 404
    
    db.session.delete(question)
    db.session.commit()
    return {"message": "Pregunta eliminada."}
  
  return {"error": "Método no permitido"}, 405  
