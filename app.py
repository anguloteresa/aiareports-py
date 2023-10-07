import os
from flask_cors import CORS
from dotenv import load_dotenv
from manage import create_app
from extensions import db

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app()
cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()