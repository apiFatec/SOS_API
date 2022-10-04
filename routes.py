from flask import Blueprint, render_template, request, redirect, url_for
import json
from models.chamados import Chamados


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
  if sala ==  "401" or sala == "402" or sala == "301" or sala == "302":
    return render_template("sala-grande/index.html", piso=num, sala=sala)
  else:
    return render_template("sala-pequena/index.html", piso=num, sala=sala)

@main.route("/abrir-chamado")
def Chamados():
  return render_template("tela-abrir-chamado/index.html")