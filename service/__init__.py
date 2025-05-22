from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

app = Flask(__name__)

# Initialize Talisman and assign to variable talisman
talisman = Talisman(app)

# Initialize CORS for the app
CORS(app)

@app.route('/')
def index():
    return "Hello, world!"
