function SubmitForm() {
  document.formulario.submit();
}

function edit(event) {
  event.preventDefault();
  nome = document.getElementById("name");
  turma = document.getElementById("turma");

  nome.style.border = "1px solid black";
  turma.style.border = "1px solid black";

  nome.style.padding = "5px";
  turma.style.padding = "5px";

  nome.disabled = false;
  turma.disabled = false;

  console.log(nome.disabled, turma.disabled);
}
