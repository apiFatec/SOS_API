function modal(id) {
  let status = document.getElementById("status" + id)
  let title = document.getElementById("title" + id)
  let data = document.getElementById("data" + id)
  let desc = document.getElementById("desc" + id)
  let cat = document.getElementById("cat" + id)
  let erro = document.getElementById("erro" + id)
  let proc = document.getElementById("proc" + id)
  let ram = document.getElementById("ram" + id)
  let win = document.getElementById("win" + id)
  let sala = document.getElementById("sala" + id)
  let numero = document.getElementById("num" + id)

  let dataModal = [
    status.innerHTML,
    title.innerHTML,
    data.innerHTML,
    desc.innerHTML,
    cat.innerHTML,
    erro.innerHTML,
    proc.value,
    ram.value,
    win.value,
    sala.value,
    numero.value
  ]
  passData(dataModal)
}

function passData(dados) {
  let status = document.getElementById("status")
  let title = document.getElementById("title")
  let data = document.getElementById("data")
  let desc = document.getElementById("desc")
  let cat = document.getElementById("cat")
  let erro = document.getElementById("cod")
  let proc = document.getElementById("proc")
  let ram = document.getElementById("ram")
  let win = document.getElementById("win")
  let end = document.getElementById("end")

  status.setAttribute('class', dados[0])
  status.innerHTML = dados[0]
  title.innerHTML = dados[1]
  desc.innerHTML = dados[3]
  cat.innerHTML = dados[4]
  erro.innerHTML = dados[5]
  data.innerHTML = dados[2]
  proc.innerHTML = dados[6]
  ram.innerHTML = dados[7]
  win.innerHTML = dados[8]
  end.innerHTML = "Endereço: " + dados[9] + " " + dados[10]

}

//  EDITAR DADOS DO CHAMADO SOMENTE SUPORTE E ADMIN

function modal_sup(id) {
  let status = document.getElementById("status" + id)
  let title = document.getElementById("title" + id)
  let data = document.getElementById("data" + id)
  let desc = document.getElementById("desc" + id)
  let cat = document.getElementById("cat" + id)
  let erro = document.getElementById("erro" + id)
  let proc = document.getElementById("proc" + id)
  let ram = document.getElementById("ram" + id)
  let win = document.getElementById("win" + id)
  let sala = document.getElementById("sala" + id)
  let numero = document.getElementById("num" + id)
  let id_chamado = document.getElementById("idChamado" + id)

  let form = document.getElementsByTagName('form')
  form[1].action = /edit_chamados/+id_chamado.value
  
  console.log(form[1].action)
  let dataModal = [
    status.innerHTML,
    title.innerHTML,
    data.innerHTML,
    desc.innerHTML,
    cat.innerHTML,
    erro.innerHTML,
    proc.value,
    ram.value,
    win.value,
    sala.value,
    numero.value
  ]
  passData_sup(dataModal)
}

function passData_sup(dados) {
  let status = document.getElementById("status")
  let title = document.getElementById("title")
  let data = document.getElementById("data")
  let desc = document.getElementById("desc")
  let cat = document.getElementById("cat")
  let erro = document.getElementById("cod")
  let proc = document.getElementById("proc")
  let ram = document.getElementById("ram")
  let win = document.getElementById("win")
  let end = document.getElementById("end")

  status.setAttribute('class', dados[0])
  status.innerHTML = dados[0]
  title.value = dados[1]
  desc.value = dados[3]
  cat.innerHTML = dados[4]
  erro.value = dados[5]
  data.innerHTML = dados[2]
  proc.innerHTML = dados[6]
  ram.innerHTML = dados[7]
  win.innerHTML = dados[8]
  end.innerHTML = "Endereço: " + dados[9] + " " + dados[10]

  // placeholder
  title.placeholder = dados[1]
  desc.placeholder = dados[3]
  erro.placeholder = dados[5]
  let inputStatus = document.getElementById('status-hidden')
  inputStatus.value = dados[0]
}

function changeStatus(statusNew) {
  let status = document.getElementById('status-hidden')
  status.value = statusNew

  console.log(status.value)
}