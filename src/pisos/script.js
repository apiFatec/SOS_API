const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const piso = urlParams.get("piso")
window.onload = function () {
  for (let i = 1; i <= 12; i++) {
    let h1 = ""
    i.toString().length < 2 ? h1 = document.getElementById("h1-0"+i) : h1 = document.getElementById("h1-"+i)
    let a = ""
    a = document.getElementById("a"+ i)
    let id = h1.id

    if (i.toString().length < 2) {
      h1.innerHTML = piso + 0 + i
    } else {
      h1.innerHTML = piso + i
    }

    let sala = ""
    i.toString().length < 2 ? sala  = piso +0+ i : sala  = piso + i

    if (id == "h1-01" || id == "h1-02") {
      a.setAttribute("href", `../sala-grande/index.html?sala=${sala}&piso=${piso}`)
    } else {
      a.setAttribute("href", `../sala-pequena/index.html?sala=${sala}&piso=${piso}`)
    }
  }
}