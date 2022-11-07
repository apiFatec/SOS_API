from email.policy import default
from db import db
import enum

from models.Adress import Address

class SisType(enum.Enum):
  old = "32"
  new = "64"

class Computador(db.Model):
  
  idComputador = db.Column(db.Integer, primary_key=True, nullable=False)
  Processador = db.Column(db.String, nullable=False)
  ram = db.Column(db.String, nullable=False)
  tipo_de_sistema = db.Column(db.String, nullable=False)
  Win_edicao = db.Column(db.String, nullable=False)
  Versao = db.Column(db.String, nullable=False)
  fk_idenderecos = db.Column(db.Integer, db.ForeignKey(Address.id_enderecos))
  chamados = db.relationship("TblChamados", backref='computador')