const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const sala = urlParams.get("sala")
const piso = urlParams.get("piso")
window.onload = () => {
  let a = document.getElementById("avoltar")
  a.setAttribute("href", `../pisos/index.html?piso=${piso}`)
}

