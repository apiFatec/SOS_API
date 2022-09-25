import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_mysqldb import MySQL

load_dotenv()
app = Flask(__name__)

app.config['MYSQL_USER'] = os.getenv("USER")
app.config['MYSQL_PASSWORD'] = os.getenv("")
app.config['MYSQL_HOST'] = os.getenv("SERVER")
app.config['MYSQL_DB'] = os.getenv("DATA_BASE")
# app.config['MYSQL_PORT'] = os.getenv("") if you use default port you don't need change this

mysql = MySQL(app)

@app.route("/")
def Home():
  cur = mysql.connection.cursor()
  cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')
  return render_template('home/index.html')

