var formClass = document.querySelectorAll(".timeTableExp");
var horary = document.querySelector(".form-element-select.horary");
var formDayClass = document.querySelectorAll(".div-form.formClass");
var deleteButton = document.querySelector(".delete-button-option");
var deleteConfirm = document.querySelector(".confirm-delete");

if (deleteButton) {
deleteButton.addEventListener('click', function() {
        deleteConfirm.classList.toggle('expand');
});
};

if(horary){
horary.addEventListener('change', function() {
    console.log('Campo de horário alterado para:', horary.value);
    formDayClass.forEach(function(formDay) { 
        formDay.classList.remove("minimize");

        if (formDay.classList.contains(horary.value)){
            formDay.classList.add("minimize");
        }
    });
});

formClass.forEach(function(formClass) {
    formClass.addEventListener('click', function() {
        
        var drop = this.closest('div.div-form.formClass');
        drop.classList.toggle('minimize');

    });
});

};

