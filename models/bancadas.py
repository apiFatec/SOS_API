from db import db

class Bancadas(db.Model):
  idBancadas = db.Column(db.Integer, primary_key=True)
  numBancadas = db.Column(db.Integer, nullable=False)
  sala = db.Column(db.String, nullable=False)
  pcBancadas = db.Column(db.Integer, nullable=False)