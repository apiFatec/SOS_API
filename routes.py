import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from models.chamados import Chamados
from models.computers import Computadores
from db import db
from models.tbl_chamados import TblChamados
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from mail import mail
from models.users import Users

main = Blueprint("routes", __name__)

s = URLSafeTimedSerializer('Thisisasecret!')

# Tela Home.
@main.route("/", methods=["GET"])
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
  return render_template("tela-abrir-chamado/index.html", pc=pc)

# Função para crair o chamado e envia-lo para o banco de dados.
# É redirecionado para a tela de chamados.
@main.route('/novo-chamado/<id>', methods=["POST", "GET"])
def Create(id):
  getPc = db.session.query(Computadores).filter_by(idComputador=id).first()
  if getPc:
    titulo = request.form.get("titulo")
    categoria = request.form.get('categoria')
    cod_erro = request.form.get('cod_erro')
    desc = request.form.get('desc')
    if titulo and categoria and desc:
      notif = request.form.get('notificar')
      if notif != None:
        notif = 1
        email = request.form.get('email')
      else: 
        email = None
        notif = 0
      chamado = TblChamados(
        titulo_chamado=titulo,
        categoria_chamado=categoria,
        cod_erro_chamado=cod_erro,
        descricao_chamado=desc,
        status_chamado="aberto",
        notificar_chamado=notif,
        email=email,
        data=insertDate(),
        fk_idComputador=id
      )
      db.session.add(chamado)
      db.session.commit()
      return render_template("tela-abrir-chamado/confirm.html")
    return redirect(url_for('routes.TelaChamados'))

# Tela de chamados.
@main.route("/chamados/", methods=["GET"])
def TelaChamados():
  chamados = Filtrar(request.args.get("status"), request.args.get("categoria"), request.args.get("search"))
  dates = getDate(chamados)
  for i in range(0, len(chamados)):
    chamados[i].data = dates[i]
  return render_template("chamados/index.html", chamados=chamados)


def Filtrar(status, categoria, search):
  # verifica se tem valor nos dois parametros e salva cada um em uma sessao.
  if status:
    session["status"] = status
  if categoria:
    session["categoria"] = categoria

  # se as duas seções tiverem valor retorna o filtro com as duas condições.
  if session.get("status") and session.get("categoria"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.status == session.get("status"), Chamados.categoria == session.get("categoria"), Chamados.titulo.like(f"%{search}%"))).all()
    else:
      chamado = Chamados.query.filter(db.and_(Chamados.status == session.get("status"), Chamados.categoria == session.get("categoria"))).all()
  # se SOMENTE status tiver um valor retorna somente chamados com o status que foi passado.
  elif session.get("status") and not session.get("categoria"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.status==session.get("status")),Chamados.titulo.like(f"%{search}%")).all()
    else:
      chamado = db.session.query(Chamados).filter_by(status=session.get("status")).all()
  #  se SOMENTE categoria tiver um valor retorna somento os chamados com a categoria.
  elif session.get("categoria") and not session.get("status"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.categoria==session.get("categoria")),Chamados.titulo.like(f"%{search}%")).all()
    else:
      chamado = db.session.query(Chamados).filter_by(categoria=session.get("categoria")).all()
  #  se as duas sessions estiverem vazias retorna todos os chamados.
  else:
    if search:
      chamado = Chamados.query.filter(Chamados.titulo.like(f"%{search}%")).all()
    else:
      chamado = db.session.query(Chamados).all()
  return chamado

# Limpa o filtro da tela de chamados.
@main.route("/limpar")
def Limpar():
  session["status"] = None
  session["categoria"] = None
  return redirect(url_for("routes.TelaChamados"))

# Pesquisar pelo nome do computador
def Search():
  chamados =  Chamados.query.filter(Chamados.titulo.like("%Sem%")).all()
  return chamados

@main.route("/novochamado")
def HomeChamado():
  sala = request.args.get("sala")
  num = request.args.get("numero")
  if len(num) == 1:
    num = "0" + num
  computador = Computadores.query.filter(db.and_(Computadores.sala==sala, Computadores.numero==num)).first()
  return render_template("tela-abrir-chamado/index.html", pc=computador)


@main.route('/<int:sala>/<int:num>/teladetalhes')
def teladetalhes(sala,num):
  comp =  Computadores.query.filter_by(sala=sala, numero=num).first()
  return render_template('tela-detalhes/index.html', comp=comp)


#Tela de atualização de detalhes de computadores

@main.route('/<id>/teladetalhes/edit', methods=['GET','POST'])
def tela_detalhes_edit(id):
  comp = Computadores.query.filter_by(idComputador=id).first()
  if request.method == 'POST':
    win = request.form['win']
    processador = request.form['processador']
    ram = request.form['ram']
    tipo_sis = request.form['tipo_sis']
    versao = request.form['versao']
    sala = request.form['sala']
    numero = request.form['numero']
    patrimonio_gabinete = request.form['patrimonio_gabinete']

    Computadores.query.filter_by(idComputador=id).update({'win':win})
    Computadores.query.filter_by(idComputador=id).update({'processador':processador})
    Computadores.query.filter_by(idComputador=id).update({'ram':ram})
    Computadores.query.filter_by(idComputador=id).update({'tipo_sis':tipo_sis})
    Computadores.query.filter_by(idComputador=id).update({'versao':versao})
    Computadores.query.filter_by(idComputador=id).update({"sala":sala})
    Computadores.query.filter_by(idComputador=id).update({"numero":numero})
    Computadores.query.filter_by(idComputador=id).update({'patrimonio_gabinete':patrimonio_gabinete})
    db.session.commit()
    return redirect(url_for('routes.teladetalhes', sala=comp.sala, num=comp.numero))
  return render_template('tela-detalhes-edit/index.html',comp=comp)


def insertDate():
  date = datetime.now().strftime("%Y %m %d %X")
  date = date.replace(" ", "-")
  date = date[:10] + " " + date[10+1:]
  return date

def getDate(chamados):
  dates = []
  for chamado in chamados:
    date = chamado.data.strftime("%d %m %Y %X")
    date = date.replace(" ", "/")
    date = date[:10] + " " + date[11:]
    dates.append(date)
  return dates



# Rota para criar um novo usuário no banco

@main.route('/cadastro', methods=["GET", "POST"])
def cadastro():
  if request.method == "POST":
    name = request.form['name']
    email = request.form['email']
    turma = request.form['turma']
    password = request.form['password'].encode('ASCII')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)

    user = Users(
      nome=name,
      email=email,
      senha=hashed,
      turma=turma
    )
    try:
      db.session.add(user)
      db.session.commit()
    except:
      return "Erro ao criar usuário"      
    return redirect(url_for('routes.created_account', email=email, name=name))
  else:
    return render_template('cadastro/index.html')


# Rota para tela de confirmar email 
# aqui chama a função para enviar o link de confirmação para o email função send_link() 
# Depois que o link é enviado para o email, o navegador é redirecionado para o email
@main.route('/created_account/<email>', defaults={'name': None}, methods=["GET", "POST"])
@main.route('/created_account/<email>/<name>', methods=["GET", "POST"])
def created_account(email, name):
  if request.method == "GET":
    return render_template('create-account-confirm/index.html', email=email, name=name)
  else:
    try:
      send_link(email)
      return redirect("https://outlook.office365.com/mail/")
    except:
      return "erro"

#  Função para enviar link de confirmação para o email
def send_link(email):
  token = s.dumps(email, salt='email-confirm')
  msg = Message('Confirm Email', sender='talison.bmc@gmail.com', recipients=[email])
  link = url_for('routes.confirm_email', token=token, email=email, _external=True)
  msg.body = f"Your link is {link}"
  mail.send(msg)


# Depois que o usuário abre o email e clica no link para confirmar
# Vem para esta rota que Valida o token e altera no banco que o email foi confirmado
@main.route('/confirm_email/<email>/<token>')
def confirm_email(email,token):
  try:
    email = s.loads(token, salt='email-confirm', max_age=900)
  except SignatureExpired:
    return "The Token is experied"
  user = Users.query.filter(Users.email == email).first()
  user.confirmed = True
  db.session.commit()
  return "The token works"



@main.route('/login', methods=["GET", "POST"])
def Login():
  if request.method == "POST":
    email = request.form['email']
    passwd = request.form['password'].encode('ASCII')
    user = db.session.query(Users).filter_by(email=email).first()
    print(user.confirmed)
    # userPass = user.senha.encode('ASCII')

    # if bcrypt.checkpw(passwd, userPass):
    #   print('match')
    # else: print("does'nt match")

    session['email'] = user.email
    session['name'] = user.nome
    session['logged'] = True

  
  return render_template("tela-login/index.html")

# Tela de usuários.
@main.route("/usuarios")
def Usuarios():
  return render_template("usuarios/index.html")

@main.route("/usuarios/edit")
def Usuarios_edit(id):
  usr = Users.query.filter_by(Usuarios=id).first()
  if request.method == 'POST':
    nome = request.form['nome']
    turma = request.form['turma']

    Users.query.filter_by(Usuarios=id).update({'nome':nome})
    Users.query.filter_by(Usuarios=id).update({'turma':turma})
    db.session.commit()
    return redirect(url_for('routes.usuarios'))
  return render_template("usuarios-edit/index.html",usr = usr)