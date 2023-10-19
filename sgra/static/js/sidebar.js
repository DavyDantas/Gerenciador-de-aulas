var menuItem = document.querySelectorAll('.item-menu');

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

var btnExp = document.querySelector('#btn-exp'); // Adicione "document." antes de querySelector
var sidebar = document.querySelector('#aside'); // Adicione "document." antes de querySelector

btnExp.addEventListener('click', function() {
    sidebar.classList.toggle('reduce');
});
