from flask import Flask, request, jsonify
import azure.functions as func
import openai
import os
import pandas as pd

app = Flask(__name__)

# OpenAI API configuration
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create dataframe for the pandas code execution
df = None
answers = []
res = ""

# code for azure funcs
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

# code for flask
@app.route('/api/test')
def test():
    return "<p>Hello, World!</p>"

@app.route('/api/upload', methods=['POST'])
def upload():
    global df  # Access the global variable
    file = request.files['file']
    df = pd.read_csv(file)
    print("File uploaded")
    # Verify columns obtained
    print("Columns")
    print(df.columns)
    # Return a response
    return jsonify({'message': 'File uploaded and processed successfully'})

# Generate questions
@app.route('/api/generate-text', methods=['POST'])
def generate_text():
    print("Generating text")
    input_text = request.json.get('input')
    response = openai.Completion.create(
        engine="test-deployment-davinci",
        prompt=str(input_text),
        temperature=0.75,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1
    )
    print(response["choices"][0]["text"])
    return response["choices"][0]["text"]


@app.route('/api/generate-code', methods=['POST'])
def generate_code():
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
    print(code)
    execute_code(code)
    print(answers)
    return answers


def execute_code(code):
    global df
    global answers
    global res
    i = 1
    
    lines = code.strip().split('%')
    
    print(lines)
    print(len(lines))
    if df is not None:
        try:
            for line in lines:
                print(i)
                i = i+1
                print(line)
                exec("global res;" + line)
                if len(res) > 1:
                    result_dict = res.to_dict()
                    answers.append(result_dict)
                else:
                    answers.append(res)
            return "Code execution successful"
        except Exception as e:
            return f"Code execution failed: {str(e)}"
            return jsonify({'message': 'DataFrame is available'})
    # Execute the generated code in another function or context
    else:
        print("No DataFrame loaded")
        return jsonify({'message': 'DataFrame is not available'})