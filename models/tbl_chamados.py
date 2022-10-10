from db import db
from models.tbl_computador import Computador

class TblChamados(db.Model):
  __tablename__ = "tbl_chamados"
  
  idChamados = db.Column(db.Integer, primary_key=True, nullable=False)
  titulo_chamado = db.Column(db.String, nullable=False)
  categoria_chamado = db.Column(db.String, nullable=False)
  cod_erro_chamado = db.Column(db.String, nullable=True)
  descricao_chamado = db.Column(db.String, nullable=False)
  status_chamado = db.Column(db.String, nullable=False)
  notificar_chamado = db.Column(db.String, nullable=True)
  fk_idComputador = db.Column(db.Integer, db.ForeignKey(Computador.idComputador))