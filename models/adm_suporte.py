from db import db
import enum

class categoria(enum.Enum):
    admin = "admin"
    suporte = "suporte"

class Suporte(db.Model):
  __tablename__ = "adm_suporte"

  idUsers_suporte = db.Column(db.Integer, primary_key=True, nullable=False)
  nome = db.Column(db.String, nullable=False)
  senha = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(120), nullable=False, unique=True)
  registro = db.Column(db.String, nullable=True)
  categoria = db.Column(db.String, default=False, nullable=True)