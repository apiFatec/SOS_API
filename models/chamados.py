from db import db

class Chamados(db.Model):
    idChamado = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    categoria = db.Column(db.String)
    cod_erro = db.Column(db.String)
    desc_chamado = db.Column(db.String)
    status = db.Column(db.String)
    notificar = db.Column(db.String)
    Processador = db.Column(db.String)
    data = db.Column(db.String)
    ram = db.Column(db.String)
    Win = db.Column(db.String)
    sala = db.Column(db.String)
    numero = db.Column(db.String)
    id_usuario = db.Column(db.String)
