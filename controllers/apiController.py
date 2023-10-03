import os
import openai
import pandas as pd
import numpy as np
from extensions import db
from flask import Flask, request, jsonify, session, render_template, current_app
from flask_restful import marshal, fields
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
from flask_cors import CORS
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

QuestionModel = {
  "id": fields.Integer,
  "question": fields.String,
  "answer": fields.String,
  "question_group_id": fields.Integer,
  "code": fields.String,
}

# Create dataframe for the pandas code execution
df = pd.read_csv('/Users/tere/Perficient/newapiwow/uploads/file.csv')
answers = []
res = ""
figure = Figure()
os.makedirs('uploads', exist_ok=True)

def loadApi():
  return {"message": "API working correctly!"}

def index():
  return render_template('index.html')

def uploadFile():
  global df
  f = request.files
  file = f["file"]
  
  # Verificar si hay archivo
  if 'file' not in f or not file.filename:
    return {"error": "No se ha proporcionado un archivo en la solicitud"}, 400

  try:
    df = pd.read_csv(file)
    filename = secure_filename(file.filename)
    session['filename'] = filename
    # Guarda la lista de diccionarios en la sesión
    df.to_csv("uploads/file.csv", index=False)
    return {"message": "Archivo subido y guardado con exito", "filename": filename}, 200
  except Exception as e:
    return {"error": "Error al procesar el archivo CSV: {}".format(str(e))}, 400

def generateText():
  global df
  print("Generating text")
  input_text = request.json.get('input')
  print(input_text)
  response = openai.Completion.create(
      engine="test-deployment-davinci",
      prompt=str(input_text),
      temperature=0.75,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      best_of=1
  )
  print(response["choices"][0]["text"])
  return response["choices"][0]["text"]

def generateQuestions():
  global df
  print("Generating text")
  input_text = request.json.get('input')
  print(input_text)
  response = openai.Completion.create(
      engine="test-deployment-davinci",
      prompt=str(input_text),
      temperature=0.75,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      best_of=1
  )
  res = response["choices"][0]["text"]
  clean = res.replace("[", "").replace("]", "").replace("'", "").strip()
  questions = [question.strip() for question in clean.split(",")]
  print(questions)
  formatted_data = []
  
  for question in questions:
    q = {"question": question, "id": None, "question_group_id":None}
    formatted_question = marshal(q, QuestionModel)
    formatted_data.append(formatted_question)
  
  print(formatted_data)
  return formatted_data

def generateGraph():
  input_text = request.json.get('input')
  response = openai.Completion.create(
    engine="test-deployment-davinci",
    prompt=str(input_text),
    temperature=0.80,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    best_of=1 
  )
  code = response["choices"][0]["text"]
  print("AI Generated Code")
  print(code)
  url = graph_code(code)
  return url

def generateCode():
  global df
  datestatus = transform_dates()
  print(datestatus)
  print("Generating code")
  input_text = request.json.get('input')
  response = openai.Completion.create(
    engine="test-deployment-davinci",
    prompt=str(input_text),
    temperature=0.80,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    best_of=1 
  )
  code = response["choices"][0]["text"]
  print("AI Generated Code")
  print(code)
  ans = execute_code(code)
  print("Status " + ans)
  print(answers)
  return answers

def transform_dates():
  global df
    
  prompt = f"""You will reply with a string of Pandas code that converts all Date columns to datetime.
      column_names = {df.columns}.
      All Date columns need to be in YYYY-MM-DD format.
      This is an example of the generated code:
          "df['Date'] = pd.to_datetime(df['Date'])
          df['Business Date'] = pd.to_datetime(df['Business Date'])"
      Reply only with Python code and Pandas. Nothing else, no comments, no notes."""
  
  response = openai.Completion.create(
      engine="test-deployment-davinci",
      prompt=str(prompt),
      temperature=0.80,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      best_of=1 
  )
  code = response["choices"][0]["text"]
  ans = transform_date(code)
  print('Status: ' + ans)
  return(code)

def transform_date(code):
    global df

    lines = code.strip().split('\n')
    print("The num of changes is : " + str(len(lines)))

    if df is not None:
        try:
            for i in range(0, len(lines), 1):
                print("Change " + str(i+1))
                print(lines[i])
                # Use eval instead of exec for safer code execution
                exec_code = compile(lines[i], '<string>', 'exec')
                exec(exec_code, globals(), locals())
            
            # Save updated dataframe
            return "Code execution successful"
        except Exception as e:
            return f"Code execution failed: {str(e)}"
    else:
        print("No DataFrame loaded")
        return "DataFrame is not available"


def graph_code(code):
  global df
  lines = code.strip().split('\n')
  print("The num of queries is : " + str(len(lines)))

  if df is not None:
    try:
      for i in range(0, len(lines), 1):
        exec(lines[i])
        # Store figure in bytes object
      buffer = BytesIO()
      FigureCanvasAgg(figure).print_png(buffer)
      # Make readable byte string for img tag
      img = base64.b64encode(buffer.getvalue()).decode()
      return img
    except Exception as e:
            return f"Code execution failed: {str(e)}"

def execute_code(code):
    global df
    global answers
    global res
    
    answers = []
    res = ''
    
    lines = code.strip().split('\n')
    print("The num of queries is : " + str(len(lines)))
    
    if df is not None:
        try:
            for i in range(0, len(lines), 1):
                print("Query " + str(i+1))
                exec("global res;" + lines[i])
                if type(res) is pd.core.series.Series:
                    result_dict = res.to_dict()
                    text = ""
                    for item in result_dict:
                        if text != "":
                            text = text + ', '
                        text = text + str(item) + ': ' + str(result_dict[item])
                    print(text)
                    answers.append(text)
                else:
                    print(res)
                    answers.append(str(res))
            return "Code execution successful"
        except Exception as e:
            return f"Code execution failed: {str(e)}"
            return jsonify({'message': 'DataFrame is available'})
    # Execute the generated code in another function or context
    else:
        print("No DataFrame loaded")
        return jsonify({'message': 'DataFrame is not available'})