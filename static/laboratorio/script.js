const pcs = document.querySelectorAll('.pc');
const dropzones = document.querySelectorAll('.dropzone');
const vazio = document.querySelector('.vazio');
const btnSalvar = document.getElementById('salvar');
const dropEdit = document.querySelectorAll('.dropEdit');

let voltarPosition = [];
let sala = dropzones[0].children[0].textContent.trim().substring(0, 3);
let notEndereco = false;

pcs.forEach(pc => {
  pc.addEventListener('dragstart', dragstart);
  pc.addEventListener('drag', drag);
  pc.addEventListener('dragend', dragend);

})

function dragstart() {
  dropzones.forEach(dropzone => dropzone.classList.add('highlight'))
  this.classList.add('is-dragging');
  // console.log(this)
}

function drag() {
}

function dragend() {
  dropzones.forEach(dropzone => dropzone.classList.remove('highlight'))
  this.classList.remove('is-dragging');
  // console.log(this)
  // essa função dragend é acionada quando vc solta o elemento dentro do dragzone
  // "this" é o elemento <a> onde tem o endereço do computador, posso alterar o endereço que fica vizivel do pc (40204) para o novo endereço e deixa-lo na cor verde para sinalizar q ele foi modificado e não foi salvo ainda.
  // terá um botão para salvar todas as modificações, quantidade de pc por bancada, bancadas e novos endereços
}

dropzones.forEach(dropzone => {
  dropzone.addEventListener('dragenter', dragenter);
  dropzone.addEventListener('dragover', dragover);
  dropzone.addEventListener('dragleave', dragleave);
  dropzone.addEventListener('drop', drop);
})

function dragenter() {

}

function dragover() {
  //  this == dropzone
  this.classList.add('over');
  // console.log(this)

  //  get draggin card

  const cardBeingDragged = document.querySelector('.is-dragging');
  if (this.children.length < 1) {
    let position = cardBeingDragged.id.substring(3,);
    let has = voltarPosition.find(pc => pc.position == position);
    if (!has) {
      if (this.classList.contains('dropEdit')) {
        voltarPosition.push({
          position: cardBeingDragged.id.substring(3,),
          content: cardBeingDragged,
          status: "Manutenção"
        })
      } else {
        voltarPosition.push({
          position: cardBeingDragged.id.substring(3,),
          content: cardBeingDragged
        })
      }
    }
    if (!this.id) {
      cardBeingDragged.childNodes[2].textContent = cardBeingDragged.id;
      cardBeingDragged.style.color = "red";
      cardBeingDragged.style.fontWeight = "bold";
      notEndereco = true;
    } else {
      let id = this.id.length == 1 ? "0" + this.id : this.id;
      cardBeingDragged.childNodes[2].textContent = sala + id;
      cardBeingDragged.style.color = "red";
      cardBeingDragged.style.fontWeight = "bold";
    }
    this.appendChild(cardBeingDragged);
    btnSalvar.style.visibility = 'visible';
  }
  console.log(voltarPosition)
}

function dragleave() {
  //  this == dropzone
  this.classList.remove('over');

}

function drop() {
  this.classList.remove('over');

}

// function voltarUm() {
//   let pc = voltarPosition.at(-1)
//   console.log(pc)
//   dropzones.forEach(dropzone => {
//     let id = dropzone.id.length == 1 ? 0 + dropzone.id : dropzone.id
//     if (pc.content.id.substring(3,) == id) {
//       //       voltarPosition.pop()
//       //     } else {
//       //       pc.content.style.color = "black"
//       //       pc.content.style.fontWeight = "normal"
//       //       pc.content.childNodes[2].textContent = sala + pc.position
//       //       console.log(pc.content.childNodes[2].textContent)
//       //       dropzone.appendChild(pc.content)
//       //       voltarPosition.pop()
//       //     }
//     }

//   })
// }

function voltarTodos() {
  btnSalvar.style.visibility = 'hidden'
  notEndereco = false
  voltarPosition.sort((a, b) => a.position - b.position);
  voltarPosition.reverse()
  dropzones.forEach(dropzone => {
    let id = dropzone.id.length == 1 ? 0 + dropzone.id : dropzone.id
    voltarPosition.forEach(pc => {
      if (pc.position == id) {

        pc.content.style.color = "black"
        pc.content.style.fontWeight = "normal"
        pc.content.childNodes[2].textContent = pc.content.id
        dropzone.appendChild(pc.content)
        voltarPosition.pop()
      }
    })
  })
}


async function alterarEndereco() {

  // dropEdit.forEach(edit => console.log(edit.innerText))

  let data = []
  dropEdit.forEach(item => {
    if (item.children.length >= 1)  data.unshift({old: item.textContent.trim(), new: "manutencao"});
    
    console.log(item.style.color == "black")
    // console.log(item.style, item)
    // item.style.color = "red"
  })
  pcs.forEach(pc => {
    // console.log(pc)
    if (pc.id != pc.innerText) {
      data.push({ old: pc.id, new: pc.innerText })
      console.log(pc)
    }
  })  
  console.log(data)
  data.sort((a,b) => {
    return a.old - b.old
  })
  console.log(data)
  const response = await fetch('http://127.0.0.1:5000/edit_layout', {
    method: 'POST', // or 'PUT'
    headers: {
      'Content-Type': 'application/json'
    },
    // redirect: 'follow',
    body: JSON.stringify(data),
  })
    .then((response) => response)
    .then((data) => {
      console.log('Success:', data);
      window.location.reload();
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  return response

}

