import os
from openai import OpenAI
import pandas as pd
from flask import request, jsonify, session
from flask_restful import marshal, fields
from werkzeug.utils import secure_filename
from io import BytesIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from dotenv import load_dotenv

# Check documentation if needed to configure the OpenAI credentials
# https://platform.openai.com/docs/api-reference

load_dotenv()

client = OpenAI(
  api_key = os.getenv("OPENAI_API_KEY")
)

QuestionModel = {
  "id": fields.Integer,
  "question": fields.String,
  "answer": fields.String,
  "question_group_id": fields.Integer,
  "code": fields.String,
}

# Create dataframe for storing the CSV
df = None
answers = []
res = ""
figure = Figure()
os.makedirs('uploads', exist_ok=True)

# Function to verify the availability of the API
def loadApi():
  return {"message": "API working correctly!"}

def uploadFile():
  global df
  f = request.files
  file = f["file"]
  
  # Verify if file exists
  if 'file' not in f or not file.filename:
    return {"error": "No se ha proporcionado un archivo en la solicitud"}, 400

  try:
    df = pd.read_csv(file)
    filename = secure_filename(file.filename)
    session['filename'] = filename
    # Save the CSV in the session of the user
    df.to_csv("uploads/file.csv", index=False)
    return {"message": "Archivo subido y guardado con exito", "filename": filename}, 200
  except Exception as e:
    return {"error": "Error al procesar el archivo CSV: {}".format(str(e))}, 400

# Endpoint to generate questions from the user's dataset
def generateQuestions():
  global df
  input_text = request.json.get('input')
  print("Generating text")
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    temperature=0.75,
    messages=[
      {"role": "system", "content": "You are a helpful assistant that generates a list of questions based on a dataset. You must return the array, with format like the following:\n['Question 1?', 'Question 2?', 'Question 3?']"},
      {"role": "user", "content": input_text}
    ]
  )
  res = completion.choices[0].message.content
  # Clean the string and convert it into the desired JSON format
  clean = res.replace("[", "").replace("]", "").replace("'", "").strip()
  questions = [question.strip() for question in clean.split(",")]
  formatted_data = []
  for question in questions:
    q = {"question": question, "id": None, "question_group_id":None}
    formatted_question = marshal(q, QuestionModel)
    formatted_data.append(formatted_question)
  print(formatted_data)
  return formatted_data

# Endpoint to generate a well-redacted executive report
def generateReport():
  global df
  print("Generating text")
  input_text = request.json.get('input')
  print(input_text)
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    max_tokens = 1000,
    messages=[
      {"role": "system", "content": "You are an insightful assistant, skilled in explaining information and writing well-redacted executive reports. You should avoid using repetitive words, and make it understandable, natural and as fluent as possible."},
      {"role": "user", "content": input_text}
    ]
  )
  res = completion.choices[0].message.content
  return res

# Endpoint to generate Pandas code to execute over the dataset to obtain results
def generateCode():
  global df
  datestatus = transform_dates()
  print(datestatus)
  print("Generating code")
  input_text = request.json.get('input')
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=[
      {"role": "system", "content": "You are a helpful assistant that generates Pandas queries to answer questions of information contained in a DataFrame. Consider dates having a datetime YYYY-MM-DD format. Follow this answer structure as an example of the expected format:\nres = df['Income'][(df['Date'].dt.month == 11)].sum()\nres = df['Money Received'][(df['Product Sold'] == 'Notebook') & (df['Sale Date'].dt.month == 2)].sum()\nres = df[(df['Seller Name'] == 'Baby Lo') & (df['Product Sold'] == 'Stapler')].groupby(df['Sale Date'].dt.year)['Units'].sum()"},
      {"role": "user", "content": input_text}
    ]
  )
  code = completion.choices[0].message.content
  print("AI Generated Code")
  print(code)
  ans = execute_code(code)
  print("Status " + ans)
  print(answers)
  return answers

# Date transformed to yyyy-mm-dd format
def transform_dates():
  global df
  prompt = f"""You will reply with a string of Pandas code that converts 'Date' columns to datetime.
      column_names = {df.columns}.
      Date columns need to be in datetime YYYY-MM-DD format.
      ONLY ATTEMPT TO CONVERT THOSE COLUMNS WHICH HAVE DATE.
      This is an example of the generated code:
          "df['Date'] = pd.to_datetime(df['Date'])
          df['Business Date'] = pd.to_datetime(df['Business Date'])"
          """
      
  user_prompt = f""" "Please convert the columns containing a date to datetime YYYY-MM-DD format. column_names = {df.columns}"""
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": user_prompt}
    ]
  )
  
  code = completion.choices[0].message.content
  ans = transform_date(code)
  print('Status: ' + ans)
  return(code)

# Date transform helper function
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

# Generate code helper function to run OpenAI's queries 
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