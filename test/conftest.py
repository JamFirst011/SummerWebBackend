import pytest
from flask import Flask
import os,sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from app.user.view import user_blueprint

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(user_blueprint)

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client