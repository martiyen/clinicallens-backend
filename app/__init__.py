from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static/dist', static_url_path='')
    
    app.config.from_object('app.config.Config')

    db.init_app(app)

    CORS(app)

    from app.routes import trials
    app.register_blueprint(trials)

    from app.scheduler import start_scheduler
    start_scheduler(app)

    with app.app_context():
        db.create_all()
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        print('Looking for index.html')
        print('App static folder is' + app.static_folder)
        return send_from_directory(app.static_folder, "index.html")

    return app
