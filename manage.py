import os
from flask import Flask
from extensions import db
from routes import api, userbp, reportbp, questionbp
from config import DevelopmentConfig, ProductionConfig, TestingConfig

def create_app():
    app = Flask(__name__)
    
    environment = os.environ.get('FLASK_ENV')

    if environment == 'development':
        print("Using Development configuration")
        app.config.from_object(DevelopmentConfig)
    elif environment == 'production':
        print("Using Production configuration")
        app.config.from_object(ProductionConfig)
    else:
        print("Using Testing configuration")
        app.config.from_object(TestingConfig)
    
    db.init_app(app)
    
    # Register your routes and blueprints here
    # from . import routes  # Import your routes here
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(userbp, url_prefix='/api/users')
    app.register_blueprint(reportbp, url_prefix='/api/reports')
    app.register_blueprint(questionbp, url_prefix='/api/questions')

    return app