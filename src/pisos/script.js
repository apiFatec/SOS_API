const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const piso = urlParams.get("piso")
window.onload = function () {
  for (let i = 1; i <= 12; i++) {
    let h1 = ""
    i.toString().length < 2 ? h1 = document.getElementById("h1-0"+i) : h1 = document.getElementById("h1-"+i)
    
    if (i.toString().length < 2) {
      h1.innerHTML = piso + 0 + i
    } else {
      h1.innerHTML = piso + i
    }
  }
}