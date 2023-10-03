import os
import openai
from flask import Flask
from extensions import db
from routes import api, userbp, reportbp, questionbp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    
    # Register your routes and blueprints here
    # from . import routes  # Import your routes here
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(userbp, url_prefix='/api/users')
    app.register_blueprint(reportbp, url_prefix='/api/reports')
    app.register_blueprint(questionbp, url_prefix='/api/questions')
    
    # Set up the OpenAI credentials
    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    return app