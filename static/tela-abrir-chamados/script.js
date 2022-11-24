
function acao_hardware(){

    let modal = document.querySelector('.modal_container_hardware')

    let software = document.querySelector(".modal_container_software")

    let rede = document.querySelector('.modal_container_rede')

    software.style.display = 'none'

    rede.style.display = 'none'

    modal.style.display = 'block';
}

function fechar_hardware(){
let fechar = document.querySelector('.modal_container_hardware')

fechar.style.display = 'none'

}

function abrir_hardware(){

    let abrir = document.querySelector('.abrir_modal_hardware')

    let fechar_soft = document.querySelector('.abrir_modal_software')

    let fechar_rede = document.querySelector('.abrir_modal_rede')

    abrir.style.display = 'inline'

    fechar_soft.style.display = 'none'

    fechar_rede.style.display = 'none'

}

function acao_software(){

    let modal = document.querySelector('.modal_container_software')

    let hardware = document.querySelector('.modal_container_hardware')

    let rede = document.querySelector('.modal_container_rede')

    hardware.style.display = 'none'

    rede.style.display = 'none'

    modal.style.display = 'block';
}

function fechar_software(){
let fechar = document.querySelector('.modal_container_software')

fechar.style.display = 'none'

}

function abrir_software(){

    let abrir = document.querySelector('.abrir_modal_software')

    abrir.style.display = 'inline'

    let fechar_hardware = document.querySelector('.abrir_modal_rede')

    fechar_hardware.style.display = 'none'

    let fechar_rede = document.querySelector('.abrir_modal_hardware')

    fechar_rede.style.display = 'none'

}


function acao_rede(){

    let modal = document.querySelector('.modal_container_rede')

    let software = document.querySelector('.modal_container_software')

    let hardware = document.querySelector('.modal_container_hardware')

    software.style.display = 'none'

    hardware.style.display = 'none'

    modal.style.display = 'block';
}

function fechar_rede(){
let fechar = document.querySelector('.modal_container_rede')

fechar.style.display = 'none'

}

function abrir_rede(){

    let abrir = document.querySelector('.abrir_modal_rede')

    let fechar_software = document.querySelector('.abrir_modal_software')

    let fechar_hardware = document.querySelector('.abrir_modal_hardware')

    abrir.style.display = 'inline'

    fechar_software.style.display = 'none'

    fechar_hardware.style.display = 'none'

}