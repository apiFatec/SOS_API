from db import db

class Relatorio(db.Model):
    idRelatorio = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    data = db.Column(db.String)
    resolucao = db.Column(db.String)
