from flask import Blueprint, render_template, request, redirect, url_for
import json

from sqlalchemy import desc
from models.chamados import Chamados
from models.computers import Computadores
from db import db


main = Blueprint("routes", __name__)

@main.route("/")
def Index():
  chamados = Chamados.query.all()
  return render_template("home/index.html", chamados=chamados)

@main.route("/fachada")
def Fachada():
  return render_template("fachada/index.html")

@main.route("/piso/<num>")
def Piso(num):
  return render_template("pisos/index.html", num=num)

@main.route("/piso/<num>/sala/<sala>")
def Sala(num, sala):
  pcs = db.session.query(Computadores).filter_by(sala=sala).all()
  if sala == "402":
    return render_template("sala-grande/sala402.html", piso=num, sala=sala, pcs=pcs)
  elif sala ==  "401" or sala == "301" or sala == "302":
    return render_template("sala-grande/index.html", piso=num, sala=sala, pcs=pcs)
  else:
    return render_template("sala-pequena/index.html", piso=num, sala=sala, pcs=pcs)

@main.route("/abrir-chamado/<id>")
def NewChamado(id):
  pc = db.session.query(Computadores).filter_by(idComputador=id).first()
  print(pc)
  return render_template("tela-abrir-chamado/index.html", pc=pc)

@main.route('/novo-chamado', methods=["POST", "GET"])
def Create():
  titulo = request.form.get("titulo")
  categoria = request.form.get('categoria')
  cod_erro = request.form.get('codigo_de_erro')
  return "" 


@main.route("/chamados")
def TelaChamado():
  chamados = db.session.query(Chamados).all()
  return render_template("chamados/index.html", chamados=chamados)