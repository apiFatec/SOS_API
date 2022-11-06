function SubmitForm() {
  document.formulario.submit();
}

function edit(event, id) {
  event.preventDefault();

  nome = document.getElementById("name" + id);
  turma = document.getElementById("turma" + id);

  iconEdit = document.getElementById("iconEdit"+id)
  iconTrash = document.getElementById("iconTrash"+id)

  btn_edit = document.getElementById("btn-edit"+id)

  if (nome.disabled && turma.disabled) {

    iconEdit.style.display = "none"
    iconTrash.style.display = "flex"

    btn_edit.style.display = "flex"

    iconTrash.style.marginTop = "16px"

    nome.style.border = "1px solid black";
    turma.style.border = "1px solid black";

    nome.style.outlineColor = "#a8bafe";
    turma.style.outlineColor = "#a8bafe";

    nome.style.padding = "5px";
    turma.style.padding = "5px";

    nome.disabled = !nome.disabled;
    turma.disabled = !turma.disabled;

  } else {

    btn_edit.style.display = "none"

    iconEdit.style.display = "flex"
    iconTrash.style.display = "none"

    nome.style.border = "none";
    turma.style.border = "none";

    nome.style.outlineColor = "#a8bafe";
    turma.style.outlineColor = "#a8bafe";

    nome.style.padding = "5px";
    turma.style.padding = "5px";

    nome.disabled = !nome.disabled;
    turma.disabled = !turma.disabled;

  }

}
