from flask import Blueprint, render_template, request, redirect, url_for, session
import json

from sqlalchemy import desc
from models.chamados import Chamados
from models.computers import Computadores
from db import db
from models.tbl_chamados import TblChamados


main = Blueprint("routes", __name__)

# Tela Home.
@main.route("/")
def Index():
  chamados = Chamados.query.all()
  return render_template("home/index.html", chamados=chamados)

# Tela fachada.
@main.route("/fachada")
def Fachada():
  return render_template("fachada/index.html")

# Função para abrir tela de pisos no andar quem o parametro <num> foi passado.
@main.route("/piso/<num>")
def Piso(num):
  return render_template("pisos/index.html", num=num)

# Função para abrir sala grande ou sala pequena dependendo dos parametros que forem passados.
@main.route("/piso/<num>/sala/<sala>")
def Sala(num, sala):
  pcs = db.session.query(Computadores).filter_by(sala=sala).all()
  if sala == "402":
    return render_template("sala-grande/sala402.html", piso=num, sala=sala, pcs=pcs)
  elif sala == "401" or sala == "301" or sala == "302":
    return render_template("sala-grande/index.html", piso=num, sala=sala, pcs=pcs)
  else:
    return render_template("sala-pequena/index.html", piso=num, sala=sala, pcs=pcs)

# Tela para abrir um novo chamado
@main.route("/abrir-chamado/<id>")
def NewChamado(id):
  pc = db.session.query(Computadores).filter_by(idComputador=id).first()
  print(pc)
  return render_template("tela-abrir-chamado/index.html", pc=pc)


# Função para crair o chamado e envia-lo para o banco de dados.
# É redirecionado para a tela de chamados.
@main.route('/novo-chamado/<id>', methods=["POST", "GET"])
def Create(id):
  titulo = request.form.get("titulo")
  categoria = request.form.get('categoria')
  cod_erro = request.form.get('cod_erro')
  desc = request.form.get('desc')
  notif = request.form.get('notificar')
  if notif != None:
    email = request.form.get('email')
  else:
    email = "none"
  chamado = TblChamados(
    titulo_chamado=titulo,
    categoria_chamado=categoria,
    cod_erro_chamado=cod_erro,
    descricao_chamado=desc,
    status_chamado="aberto",
    notificar_chamado=0,
    fk_idComputador=id
  )
  db.session.add(chamado)
  db.session.commit()

  return redirect(url_for('routes.TelaChamado'))

# Tela de chamados.
@main.route("/chamados", methods=["GET"])
def TelaChamado():
  chamados = Filtrar(request.args.get("status"), request.args.get("categoria"))
  return render_template("chamados/index.html", chamados=chamados)


def Filtrar(status, categoria):
  # verifica se tem valor nos dois parametros e salva cada um em uma sessao.
  if status:
    session["status"] = status
  if categoria:
    session["categoria"] = categoria

  # se as duas seções tiverem valor retorna o filtro com as duas condições.
  if session.get("status") and session.get("categoria"):
    chamado = Chamados.query.filter(db.and_(Chamados.status == session.get("status"), Chamados.categoria == session.get("categoria"))).all()
    return chamado
  # se SOMENTE status tiver um valor retorna somente chamados com o status que foi passado.
  elif session.get("status") and not session.get("categoria"):
    chamado = db.session.query(Chamados).filter_by(status=session.get("status")).all()
  #  se SOMENTE categoria tiver um valor retorna somento os chamados com a categoria.
  elif session.get("categoria") and not session.get("status"):
    chamado = db.session.query(Chamados).filter_by(categoria=session.get("categoria")).all()
  #  se as duas sessions estiverem vazias retorna todos os chamados.
  else:
    chamado = db.session.query(Chamados).all()
  return chamado

# Limpa o filtro da tela de chamados.
@main.route("/limpar")
def Limpar():
  session["status"] = None
  session["categoria"] = None
  return redirect(url_for("routes.TelaChamado"))

# Pesquisar pelo nome do computador