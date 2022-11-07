from db import db

class Address(db.Model):
  __tablename__ = "enderecos"

  id_enderecos = db.Column(db.Integer, primary_key=True, nullable=False)
  sala = db.Column(db.String, nullable=False)
  numero = db.Column(db.String, nullable=False)
  patrimonio_gabinete = db.Column(db.String, nullable=True)
  patrimonio_monitor = db.Column(db.String, nullable=True)
  computador = db.relationship("Computador", backref="address", lazy='dynamic')