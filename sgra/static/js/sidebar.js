var menuItem = document.querySelectorAll('.item-menu');
var dropdown = document.querySelectorAll('.dropdown');
var navDrop = document.querySelectorAll('.nav-drop');
var dropItem = document.querySelectorAll('.item-drop');
var btnExp = document.querySelector('#btn-exp'); // Adicione "document." antes de querySelector
var sidebar = document.querySelector('#aside'); // Adicione "document." antes de querySelector


function selectLink(event) {
    event.preventDefault(); // Evita o comportamento padrão do link

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

btnExp.addEventListener('click', function() {
    sidebar.classList.toggle('reduce');
    
    dropdown.forEach(function(item) {
        if (item.classList.contains('down')) {
            item.classList.remove('down');
        }
    });
});

navDrop.forEach(function(navDrop) {
    navDrop.addEventListener('click', function(event) {
        event.preventDefault(); // Evita o comportamento padrão do link
        
        // Obtém o elemento 'li' pai do elemento 'a' clicado
        var drop = this.closest('li.dropdown');
        // Adiciona a classe 'down' ao 'dropdown' associado
        drop.classList.toggle('down');

        if(sidebar.classList.contains('reduce')){
            sidebar.classList.remove('reduce');
        }

    });
});