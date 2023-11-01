formClass = document.querySelectorAll(".timeTableExp")
horary = document.querySelector(".form-element-select.horary")
formDayClass = document.querySelectorAll(".div-form.formClass")

horary.addEventListener('change', function(){
    console.log(horary.value)
    formDayClass.forEach(function(formDayClass){

        formDayClass.classList.remove("minimize")

        if (formDayClass.classList.contains(horary.value)){
            
            formDayClass.classList.add("minimize")
        }

    });
});

formClass.forEach(function(formClass) {
    formClass.addEventListener('click', function(event) {
        
        // Obtém o elemento 'li' pai do elemento 'a' clicado
        var drop = this.closest('div.div-form.formClass');
        drop.classList.toggle('minimize');

    });
});