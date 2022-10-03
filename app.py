from dotenv import load_dotenv
from flask import Flask
from routes import main
from db import db
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(main)

if __name__ == "__main__": 
  app.run()