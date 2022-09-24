const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)

window.onload = () => {
  if (urlParams.get("status") == "true") {
    let modal = document.getElementById("modal")
    modal.style.display = "flex"
  }
}

function modal() {
  let modal = document.getElementById("modal")
    modal.style.display = "none"
}