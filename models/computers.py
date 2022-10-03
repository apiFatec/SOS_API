from db import db
import enum

class SisType(enum.Enum):
  old = "32"
  new = "64"

class Computers(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False)
  Processador = db.Column(db.String, nullable=False)
  ram = db.Column(db.String, nullable=False)
  tipo_sis = db.Column(enum.Enum(SisType), nullable=False)
  Win = db.Column(db.String, nullable=False)
  Versao = db.Column(db.String, nullable=False)
  idEndereco = db.Comlumn(db.Integer, db.ForeignKey("address.id"), nullable=False)


