from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

def listarProfessores(request):
    teachers = Teacher.objects.all()
    return render(request,'listaProfessores.html', {'teachers':teachers})

def listarTurmas(request):

    courses = categoryCourse.objects.all()
    context = {'courses':courses}

    return render(request, "listaTurmas.html", context)

def teacherForm(request):

    if request.method == "GET":
        teachers = Teacher.objects.all()
        form = formsTeacher()
        
    
    else:
        form = formsTeacher(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('FormTeacher')

    context={
        'form': form,
        'teachers': teachers,
        }
    return render(request, "formsProfessor.html", context)

def subjectForm(request):

    subjects = Subject.objects.all()
    if request.method == "GET":
        form = formsSubject()
        
    
    else:
        form = formsSubject(request.POST)
        if form.is_valid():
            form.save()
            return redirect('FormSubject')

    context={
        'form': form,
        'subjects': subjects,
        }
    return render(request, "formsDisciplina.html", context)

def classForm(request):
    courses = categoryCourse.objects.all()

    if request.method == "GET":
        courseForm = formsCourse()
        formClass = formsClass()
        dayClasses_list = [formsDayClasses(prefix=str(i)) for i in range(5)]
        for i, dayClasses in enumerate(dayClasses_list):
            if i == 0:
                dayClasses.day = 'Segunda-feira'
            elif i == 1:
                dayClasses.day = 'Terça-feira'
            elif i == 2:
                dayClasses.day = 'Quarta-feira'
            elif i == 3:
                dayClasses.day = 'Quinta-feira'
            elif i == 4:
                dayClasses.day = 'Sexta-feira'



    else:
        courseForm = formsCourse(request.POST)
        formClass = formsClass(request.POST)
        dayClasses_list = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5)]

        if courseForm.is_valid():
            print("\nFORMULARIO CORRETO CURSO\n")
            courseForm.save()
            return redirect('FormClass')
        
        if formClass.is_valid():
            courseForm.cleaned_data()
            formSaveClass = formClass.save(commit=False)
            print("\nFORMULARIO CORRETO\n")
            if all([form.is_valid() for form in dayClasses_list]):
                print("\nVERIFICANDO VALIDADE AULAS\n")
                for form in dayClasses_list:
                    new_form = form.save(commit=False)
                    new_form.classObj = formSaveClass
                    new_form.save()
            formClass.save()
            return redirect('FormClass')
        
    context = {
        'formClass': formClass,
        'dayClasses_list': dayClasses_list,
        'courseForm': courseForm,
        'courses':  courses,
    }

    return render(request, 'formsTurma.html', context)


        
