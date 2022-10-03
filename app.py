from dotenv import load_dotenv
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from routes import main

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

app.register_blueprint(main)

if __name__ == "__main__": 
  app.run()