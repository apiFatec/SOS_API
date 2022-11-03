from db import db

class Users(db.Model):
  __tablename__ = "usuarios"

  id_usuario = db.Column(db.Integer, primary_key=True, nullable=False)
  nome = db.Column(db.String, nullable=False)
  senha = db.Column(db.String(72), nullable=False)
  email = db.Column(db.String, nullable=False)