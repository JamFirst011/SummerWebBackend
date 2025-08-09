from flask import Flask
from flask_cors import CORS
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, 'dist')

def create_app():
    app = Flask(__name__,static_url_path='',static_folder=DIST_DIR)
    CORS(app)

    from app.user.view import user_blueprint
    from app.post.view import post_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(post_blueprint)


    return app