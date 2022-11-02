const pcs = document.querySelectorAll('.pc')
const dropzones = document.querySelectorAll('.dropzone')
const vazio = document.querySelector('.vazio')

pcs.forEach(pc => {
  pc.addEventListener('dragstart', dragstart)
  pc.addEventListener('drag', drag)
  pc.addEventListener('dragend', dragend)
})

function dragstart() {
  dropzones.forEach(dropzone => dropzone.classList.add('highlight'))
  this.classList.add('is-dragging')
}

function drag() {

}

function dragend() {
  dropzones.forEach(dropzone => dropzone.classList.remove('highlight'))
  this.classList.remove('is-dragging')
}

dropzones.forEach(dropzone => {
  dropzone.addEventListener('dragenter', dragenter)
  dropzone.addEventListener('dragover', dragover)
  dropzone.addEventListener('dragleave', dragleave)
  dropzone.addEventListener('drop', drop)
})

function dragenter() {
  
}

function dragover() {
  //  this == dropzone
  this.classList.add('over')

  //  get draggin card
  const cardBeingDragged = document.querySelector('.is-dragging')
console.log(this.children.length)
  if (this.children.length < 1) {
    this.appendChild(cardBeingDragged)
  }
}

function dragleave() {
  //  this == dropzone
  this.classList.remove('over')

}

function drop() {
  this.classList.remove('over')

}