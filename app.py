from dotenv import load_dotenv
from flask import Flask
from routes import main
from flask_session import Session
from db import db
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)

app.register_blueprint(main)

if __name__ == "__main__": 
  app.run(debug=True)