from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from models.Adress import Address
from models.adm_suporte import Suporte
from models.bancadas import Bancadas
from models.chamados import Chamados
from models.computers import Computadores
from db import db
from models.tbl_chamados import TblChamados
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from mail import mail
from models.tbl_computador import Computador
from models.users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from models.relatorio import Relatorio

main = Blueprint("routes", __name__)

s = URLSafeTimedSerializer('Thisisasecret!')

# Tela Home.
@main.route("/", methods=["GET"])
def Index():
  chamados = Chamados.query.order_by(Chamados.idChamado.desc()).limit(8).all()
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
  outPc = []
  pcs = db.session.query(Computadores).filter_by(sala=sala).all()
  for pc in pcs:
    if pc.out:
      outPc.append(pc)

  if len(pcs) > 0:
    bancada = db.session.query(Bancadas).filter_by(sala=sala).first()
    qtBancadas = bancada.numBancadas
    qtPcBancada = bancada.pcBancadas

    if qtBancadas <= ceil((len(pcs) - 1)/qtPcBancada):
      qtBancadas = ceil((len(pcs) - 1)/qtPcBancada)
      bancada.numBancadas = qtBancadas
      db.session.commit()
    return render_template("laboratorio/index.html", piso=num, sala=sala, pcs=pcs, bancadas=qtBancadas, qtPc=qtPcBancada, outPc=outPc)
  else:
    return render_template('sala-aula/index.html', piso=num)
  

# Tela para abrir um novo chamado
@main.route("/abrir-chamado/<id>")
def NewChamado(id):
  if not session.get('verified') and session.get('logged'):
    return redirect(url_for('routes.created_account', email=session.get('email'), name=session.get('name')))
  else:
    pc = db.session.query(Computadores).filter_by(idComputador=id).first()
    return render_template("tela-abrir-chamado/index.html", pc=pc)


# Função para crair o chamado e envia-lo para o banco de dados.
# É redirecionado para a tela de chamados.
@main.route('/novo-chamado/<id>', methods=["POST", "GET"])
def Create(id):
  getPc = db.session.query(Computadores).filter_by(idComputador=id).first()
  user = db.session.query(Users).filter_by(email=session.get('email')).first()
  if user:
    id_usuario = user.id_usuario
  else: id_usuario = 0
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
        status_chamado="Aberto",
        notificar_chamado=notif,
        email=email,
        data=insertDate(),
        fk_idComputador=id,
        fk_idUsuario=id_usuario
      )
      getPc.status = 'Aberto'
      db.session.add(chamado)
      db.session.commit()
      return render_template("tela-abrir-chamado/confirm.html")
    return redirect(url_for('routes.TelaChamados'))

# Tela de chamados.
@main.route("/chamados/", methods=["GET"])
def TelaChamados():
  chamados = Filtrar(request.args.get("status"), request.args.get("categoria"), request.args.get("search"))
  dates = getDates(chamados)
  for i in range(0, len(chamados)):
    chamados[i].data = dates[i]
  page = request.args.get('page', 1, type=int)
  pagination = Chamados.query.filter_by().paginate(page, per_page=8)
  return render_template("chamados/index.html", chamados=chamados, searched_for=request.args.get("search"), len=len(chamados), pagination=pagination, page=page)


def Filtrar(status, categoria, search):
  # verifica se tem valor nos dois parametros e salva cada um em uma sessao.
  if status:
    session["status"] = status
  if categoria:
    session["categoria_chamado"] = categoria

  

  # se as duas seções tiverem valor retorna o filtro com as duas condições.
  if session.get("status") and session.get("categoria_chamado"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.status == session.get("status"), Chamados.categoria == session.get("categoria_chamado"), Chamados.titulo.like(f"%{search}%"))).all()
    else:
      chamado = Chamados.query.filter(db.and_(Chamados.status == session.get("status"), Chamados.categoria == session.get("categoria_chamado"))).all()
  # se SOMENTE status tiver um valor retorna somente chamados com o status que foi passado.
  elif session.get("status") and not session.get("categoria_chamado"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.status==session.get("status")),Chamados.titulo.like(f"%{search}%")).all()
    else:
      chamado = db.session.query(Chamados).filter_by(status=session.get("status")).all()
  #  se SOMENTE categoria tiver um valor retorna somento os chamados com a categoria.
  elif session.get("categoria_chamado") and not session.get("status"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.categoria==session.get("categoria_chamado")),Chamados.titulo.like(f"%{search}%")).all()
    else:
      chamado = db.session.query(Chamados).filter_by(categoria=session.get("categoria_chamado")).all()
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
  session["categoria_chamado"] = None
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
    compOut =  Computadores.query.filter_by(oldLocale=f"{sala}"+f"{num}", out=True).first()
    if compOut:
      return render_template('tela-detalhes/index.html', comp=compOut)
    else:
      comp =  Computadores.query.filter_by(sala=sala, numero=num).first()
      return render_template('tela-detalhes/index.html', comp=comp)
  


#Tela de atualização de detalhes de computadores

@main.route('/<id>/teladetalhes/edit', methods=['GET','POST'])
def tela_detalhes_edit(id):
  if session.get('categoria') == 'suporte' or session.get('categoria') == 'admin':
    comp = Computadores.query.filter_by(idComputador=id).first()
    if comp.out:
      comp.numero = comp.oldLocale[3:] + " em manutenção"

    if request.method == 'POST':
      win = request.form['win']
      processador = request.form['processador']
      ram = request.form['ram']
      tipo_sis = request.form['tipo_sis']
      versao = request.form['versao']
      sala = request.form['sala']
      numero = request.form['numero']
      patrimonio_gabinete = request.form['patrimonio_gabinete']
      # if comp.sala == sala and comp.numero == numero:
      has_pc = Computadores.query.filter(db.and_(Computadores.sala == sala, Computadores.numero == numero)).first()

      if comp.sala == sala and comp.numero == numero:
        Computadores.query.filter_by(idComputador=id).update({'win':win})
        Computadores.query.filter_by(idComputador=id).update({'processador':processador})
        Computadores.query.filter_by(idComputador=id).update({'ram':ram})
        Computadores.query.filter_by(idComputador=id).update({'tipo_sis':tipo_sis})
        Computadores.query.filter_by(idComputador=id).update({'versao':versao})
        Computadores.query.filter_by(idComputador=id).update({'patrimonio_gabinete':patrimonio_gabinete})
        db.session.commit()
        return redirect(url_for('routes.teladetalhes', sala=comp.sala, num=comp.numero))
      else:
        # verificar se 
        ""


      if not has_pc: 
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
  return redirect(url_for('routes.Index'))


def insertDate():
  date = datetime.now().strftime("%Y %m %d %X")
  date = date.replace(" ", "-")
  date = date[:10] + " " + date[10+1:]
  return date

def getDates(chamados):
  dates = []
  for chamado in chamados:
    date = chamado.data.strftime("%d %m %Y %X")
    date = date.replace(" ", "/")
    date = date[:10] + " " + date[11:]
    dates.append(date)
  return dates

def getDate(chamado):
  date = chamado.data.strftime("%d %m %Y %X")
  date = date.replace(" ", "/")
  date = date[:10] + " " + date[11:]
  return date



# Rota para criar um novo usuário no banco

@main.route('/cadastro', methods=["GET", "POST"])
def cadastro():
  session['notFatec'] = False
  if request.method == "POST":
    name = request.form['name']
    turma = request.form['turma']
    password = request.form['password']
    hashed = generate_password_hash(password, method='sha256')
    email = request.form['email']
    if "@fatec.sp.gov.br" not in email:
      session['notFatec'] = True
      return render_template('cadastro/index.html')
    
    user = Users(
      nome=name,
      email=email,
      senha=hashed,
      turma=turma,
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
  session['verified'] = True
  db.session.commit()
  return redirect(url_for('routes.confirmed_email', name=user.nome))

@main.route('/confirmed_email/<name>')
def confirmed_email(name):
  return render_template('create-account-confirm/confirmed.html', name=name)

@main.route('/login', methods=["GET", "POST"])
def Login():
  session['errorMail'] = False
  session['errorPassword'] = False
  if request.method == "POST":
    email = request.form['email']
    senha = request.form['password']
    user = Users.query.filter_by(email=email).first()

    if user:
      if check_password_hash(user.senha, senha):
        login_user(user)
        return redirect(url_for('routes.Index'))
      else:
        session['errorPassword'] = True
        return render_template('tela-login/index.html')
    if email == "suporte.sjc@fatec.com":
      user_sup = Suporte.query.filter_by(email=email).first()
      if check_password_hash(user_sup.senha, senha):
        login_sup(user_sup)
        return redirect(url_for('routes.Index'))
    else:
      session['errorMail'] = True
      return render_template('tela-login/index.html')



  return render_template("tela-login/index.html")
  
@main.route('/logout')
def Logout():
  logout_user()
  return redirect(url_for('routes.Index'))

def login_user(user):
  session['name'] = user.nome
  session['email'] = user.email
  session['logged'] = True
  session['verified'] = user.confirmed
  session['id_user'] = user.id_usuario

def login_sup(user):
  session['name'] = user.nome
  session['email'] = user.email
  session['logged'] = True
  session['categoria'] = user.categoria
  session['verified'] = True
  session['id_user'] = user.idUsers_suporte


def logout_user():
  session.clear()


# Tela de usuários.
@main.route("/usuarios")
def Usuarios():
  users = db.session.query(Users).all()
  return render_template("usuarios/index.html", users=users)

@main.route("/usuarios/edit/<id>", methods=["GET", "POST"])
def Usuarios_edit(id):
  usr = Users.query.filter_by(id_usuario=id).first()
  if request.method == 'POST':
    nome = request.form['name']
    turma = request.form['turma']

    Users.query.filter_by(id_usuario=id).update({'nome':nome})
    Users.query.filter_by(id_usuario=id).update({'turma':turma})
    db.session.commit()
    return redirect(url_for('routes.Usuarios'))
  return render_template("usuarios-edit/index.html",usr = usr)


# -------------------------------------------------------------------------------------------------
#  FILTRO DOS CHAMADOS DE UM USUÁRIO LOGADO
# -------------------------------------------------------------------------------------------------
@main.route('/meus_chamados', defaults={'id': None})
@main.route('/meus_chamados/<id>')
def meus_chamados(id):
  if not session.get('logged'):
    return redirect(url_for("routes.Index"))
  if id:
    chamados = Chamados.query.filter_by(idChamado=id).first()
    search = chamados.titulo
    chamados.data = getDate(chamados)
    chamados = [chamados]
    print(chamados)
  else: 
    search = request.args.get("search")
    chamados = meus_chamados_filter(request.args.get("status"), request.args.get("categoria"), search)
    dates = getDates(chamados)
    for i in range(0, len(chamados)):
      chamados[i].data = dates[i]

  return render_template('meus-chamados/index.html', chamados=chamados, searched_for=search, len=len(chamados))


def meus_chamados_filter(status, categoria, search):
  # verifica se tem valor nos dois parametros e salva cada um em uma sessao.
  if status:
    session["status"] = status
  if categoria:
    session["categoria"] = categoria

  # se as duas seções tiverem valor retorna o filtro com as duas condições.
  
  if session.get("status") and session.get("categoria_chamado"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.status == session.get("status"), Chamados.categoria == session.get("categoria_chamado"), Chamados.titulo.like(f"%{search}%"), Chamados.id_usuario == session.get('id_user'))).all()
    else:
      chamado = Chamados.query.filter(db.and_(Chamados.status == session.get("status"), Chamados.categoria == session.get("categoria_chamado"), Chamados.id_usuario == session.get('id_user'))).all()
  # se SOMENTE status tiver um valor retorna somente chamados com o status que foi passado.
  elif session.get("status") and not session.get("categoria_chamado"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.status==session.get("status"),Chamados.titulo.like(f"%{search}%"), Chamados.id_usuario == session.get('id_user'))).all()
    else:
      chamado = Chamados.query.filter(db.and_(Chamados.status == session.get('status'), Chamados.id_usuario == session.get('id_user'))).all()
  #  se SOMENTE categoria tiver um valor retorna somento os chamados com a categoria.
  elif session.get("categoria_chamado") and not session.get("status"):
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.categoria==session.get("categoria_chamado")), Chamados.id_usuario == session.get('id_user')).all()
    else:
      chamado = Chamados.query.filter(db.and_(Chamados.categoria == session.get('categoria')), Chamados.id_usuario == session.get('id_user')).all()
  #  se as duas sessions estiverem vazias retorna todos os chamados.
  else:
    if search:
      chamado = Chamados.query.filter(db.and_(Chamados.titulo.like(f"%{search}%"), Chamados.id_usuario == session.get('id_user'))).all()
    else:
      chamado = db.session.query(Chamados).filter_by(id_usuario=session.get('id_user')).all()
  return chamado

@main.route("/limpar_meu_chamado")
def Limpar_meu_chamado():
  session["status"] = None
  session["categoria"] = None
  return redirect(url_for("routes.meus_chamados"))


@main.route('/edit_chamados/<id>', methods=["post"])
def edit_chamados(id):
  chamado = TblChamados.query.filter_by(idChamados=id).first()
  chamado.titulo_chamado = request.form.get('title')
  chamado.cod_erro_chamado = request.form.get('error')
  chamado.descricao_chamado = request.form.get('desc')
  chamado.status_chamado = request.form.get('status-hidden')
  pc = Computador.query.filter_by(idComputador=chamado.fk_idComputador).first()
  pc.status = request.form.get('status-hidden')

  if chamado.email:
    send_notif(chamado.email,request.form.get('status-hidden'),chamado.idChamados)
  db.session.commit()
  return redirect(url_for('routes.TelaChamados'))


def send_notif(email,status,id):
  msg = Message('SOS FATEC', sender='wedevtm@gmail.com', recipients=[email])
  link = url_for('routes.meus_chamados', searched_for=id, _external=True)
  msg.body = f'''
  Olá estamos entrando em contato para te informar que temos atualizações sobre o chamado que você abriu no SOS FATEC o status dele foi alterado para: {status}
  link para visualizar o chamado {link}
  '''
  mail.send(msg)

@main.route('/contato')
def contato():
  return render_template('contato/index.html')

@main.route('/adicionar_computador', methods=["GET", "POST"])
def adicionar_computador():
  if request.method == "POST":
    sala = request.form.get('sala')
    num = request.form.get('num')

    computador = Computadores.query.filter(db.and_(Computadores.sala == sala , Computadores.numero == num)).first()
    if not computador:
      proc = request.form.get('proc')
      ram = request.form.get('ram')
      type_sys = request.form.get('type_sys')
      win_edition = request.form.get('win_edition')
      version = request.form.get('version')
      pat_mon = request.form.get('pat_mon')
      pat_gab = request.form.get('pat_gab')
      
      address = Address(
        sala=sala,
        numero=num,
      )

      newPC = Computador(
        Processador=proc,
        ram=ram+".00 GB",
        tipo_de_sistema=type_sys,
        Win_edicao=win_edition,
        Versao=version
      )
      address.computador.append(newPC)
      db.session.add(newPC)
      db.session.add(address)
      db.session.commit()
    print(computador)

  return render_template('add-pc/index.html')

@main.route('/relatorio', methods=["GET", "POST"])
def relatorio():
  if request.method == "POST":
    nome = request.form.get('nome')
    data = request.form.get('data')
    resolucao = request.form.get('resolucao')
   
    relatorio = Relatorio(
      nome=nome,
      data=data,
      resolucao=resolucao
    )

    db.session.add(relatorio)
    db.session.commit()
    print(relatorio)
    return render_template('home/index.html')
  
 
  return render_template('relatorio/index.html')
  

@main.route('/teste')
def teste():
  pcs = db.session.query(Computadores).filter_by(sala='402').all()
  return render_template('teste/index.html', pcs=pcs)

@main.route('/edit_layout', methods=['POST', 'GET'])
def editLayout():
  if request.method == "POST":
    for alterPc in request.get_json(force=True):
      if alterPc['new'] == "manutencao":
        outPc = Computadores.query.filter(db.and_(Computadores.sala ==alterPc['old'][:3] , Computadores.oldLocale == alterPc['old'])).first()
        if outPc:
          outPc.out = True
          outPc.oldLocale = alterPc['old']
          outPc.numero = ""
          print("oldlocal")
      else:
        pc = Computadores.query.filter(db.and_(Computadores.sala ==alterPc['old'][:3] , Computadores.numero == alterPc['old'][3:])).first()
        hasPc = Computadores.query.filter(db.and_(Computadores.sala ==alterPc['new'][:3] , Computadores.numero == alterPc['new'][3:])).first()
        if not hasPc:
          print("haspc")
          pc.sala = alterPc['new'][:3]
          pc.numero = alterPc['new'][3:]
          print("foi")
        else: print("nao foi")
      db.session.commit()
    return ""
  else: 
    return ""
