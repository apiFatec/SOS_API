from db import db
import enum

class Computadores(db.Model):
  idComputador = db.Column(db.Integer, primary_key=True)
  processador = db.Column(db.String)
  ram = db.Column(db.String)
  tipo_sis = db.Column(db.String)
  win = db.Column(db.String)
  versao = db.Column(db.String)
  sala = db.Column(db.String)
  numero = db.Column(db.String)
  patrimonio_gabinete = db.Column(db.String)
  patrimonio_monitor = db.Column(db.String)
  status = db.Column(db.String, nullable=False)
  out = db.Column(db.Boolean)
  oldLocale = db.Column(db.String)


