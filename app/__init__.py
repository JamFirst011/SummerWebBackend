from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.user.view import user_blueprint
    from app.post.view import post_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(post_blueprint)

    return app