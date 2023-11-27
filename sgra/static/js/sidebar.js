var menuItem = document.querySelectorAll('.item-menu');
var dropdown = document.querySelectorAll('.dropdown');
var navDrop = document.querySelectorAll('.nav-drop');
var dropItem = document.querySelectorAll('.item-drop');
var btnExp = document.querySelector('#btn-exp'); // Adicione "document." antes de querySelector
var sidebar = document.querySelector('#aside'); // Adicione "document." antes de querySelector
var mainBody = document.querySelector('.main-body');

function selectLink(event) {
    menuItem.forEach((item) =>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo');

}

menuItem.forEach((item) =>
    item.addEventListener('click', selectLink)
)

function selectLinkDrop(_event) {

    dropItem.forEach((item) =>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo');
}

dropItem.forEach((item) =>
    item.addEventListener('click', selectLinkDrop)
)
//Responsavel por mover o body ao reduzir a sidebar por reduzir a sidebar ao clicar no botão de reduzir
btnExp.addEventListener('click', function() {
    if (sidebar.classList.contains('reduce')){
        sidebar.classList.remove('reduce');
        mainBody.classList.remove('margin-left');
        localStorage.setItem('sidebarState', ' ');
    }
    else{
    sidebar.classList.add('reduce');
    mainBody.classList.add('margin-left');
    localStorage.setItem('sidebarState', 'reduce');
    }
    dropdown.forEach(function(item) {
        if (item.classList.contains('down')) {
            item.classList.remove('down');
        }
    });
});



navDrop.forEach(function(navDrop) {
    navDrop.addEventListener('click', function(event) {
        
        // Obtém o elemento 'li' pai do elemento 'a' clicado
        var drop = this.closest('li.dropdown');
        drop.classList.toggle('down');

        if(sidebar.classList.contains('reduce')){
            mainBody.classList.remove('margin-left');
            sidebar.classList.remove('reduce');
        }

    });
});




  // Função para expandir a barra lateral
  function expandSidebar() {
    // Adicione a classe 'expandida' ao elemento da barra lateral
    sidebar.classList.remove('reduce');
    // Armazene o estado no localStorage
    localStorage.setItem('sidebarState', ' ');
    mainBody.classList.remove('margin-left');
  }

  // Função para reduzir a barra lateral
  function reduceSidebar() {
    // Remova a classe 'expandida' do elemento da barra lateral
    sidebar.classList.add('reduce');
    // Armazene o estado no localStorage
    localStorage.setItem('sidebarState', 'reduce');
    mainBody.classList.add('margin-left');
  }

  // Verifique o estado armazenado no localStorage ao carregar a página
  window.addEventListener('load', function() {
    const sidebarState = localStorage.getItem('sidebarState');
    if (sidebarState === ' ') {
      expandSidebar();

    } else if (sidebarState === 'reduce') {
      reduceSidebar();
    }
  });