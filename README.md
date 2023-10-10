# AI Assisted Reports RESTful API

A custom Flask RESTful API for the [AI Assisted Reports](https://aiareports2.azurewebsites.net/) Perficient app.

## About this project

This API generates insightful reports from datasets with the use of Azure's OpenAI model.

## How it works
1. The dataset columns are passed to the model, which generates questions that can be answered from the data.
2. The user can add, edit or delete the questions.
3. The questions are passed again to the API. Pandas code is generated and executed to answer the queries.
4. The user can make individual queries again, or generate the final report.
5. The model generates a report that the user can check and modify.

## Running locally

This API is built with [Python 3.11](https://www.python.org/downloads/). Install it before attempting to run the API.

1. Clone the project repository.

```sh
git clone git@github.com:anguloteresa/aiareports-py.git
cd aiareports-py
```

2. Create a virtual environment and install all required dependencies.

> You can find a detailed guide on Python virtual environments [here](https://docs.python.org/3/library/venv.html).

```sh
pip install virtualenv
virtualenv env
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a .env file and set up your OpenAI API credentials. The structure is shown below.

```env
SECRET_KEY='Your-secret-key'
OPENAI_API_BASE='your-openai-base'
OPENAI_API_KEY='your-openai-key'
OPENAI_API_TYPE='your-openai-type'
OPENAI_API_VERSION='YYYY-MM-DD'
```

4. Run the API.

```
python app.py
```

Your app will run in `127.0.0.1:5000`.

## Routes

| Route            | Description                                        |
| ---------------- | -------------------------------------------------- |
| `api/`           | Main API functionality (OpenAI calls, dataset load)|
| `api/users/`     | Login, user administration (create, edit, update)  |
| `api/questions/` | Question and question group controller             |
| `api/reports/`   | Report controller                                  |


## Usage examples

All POST calls take a JSON file as an input, so be sure to pass your data in that format.

For instance, call for creating a Question Group will be:

`[POST] 127.0.0.1:5000/api/questions/groups/create`

```json
{
  "name": "Employee Dataset Questions",
  "owner": "37"
}
```