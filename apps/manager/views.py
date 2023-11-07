from django.shortcuts import render, redirect
from .models import Class, dayClasses, Teacher, Subject, categoryCourse
from .forms import *
from django.contrib import messages

# Create your views here.
def Login(request):

    return render(request, "login.html")

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

def courseForm(request):

    courses = categoryCourse.objects.all()
    if request.method == "GET":
        form = formsCourse()
        
    
    else:
        form = formsCourse(request.POST)
        if form.is_valid():
            form.save()
            return redirect('FormCourse')

    context={
        'form': form,
        'courses': courses,
        }
    return render(request, "formsCurso.html", context)

dayCla = dayClasses
def classForm(request):

    classes = Class.objects.all()
    days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
            'Quinta-feira','Sexta-feira']

    if request.method == "GET":

        
        formClass = formsClass()

        
        dayClasses_list_morning = [formsDayClasses(prefix=str(i)) for i in range(0,5)]
        dayClasses_list_afternoon = [formsDayClasses(prefix=str(i)) for i in range(5,10)]
        dayClasses_list_night = [formsDayClasses(prefix=str(i)) for i in range(10, 15)]
        for i, dayClasse in enumerate(dayClasses_list_morning):
            dayClasse.day = days[i]
            dayClasses_list_afternoon[i].day = days[i]
            dayClasses_list_night[i].day = days[i]
                


    else:
        
        formClass = formsClass(request.POST)
        dayClasses_list_morning = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5)]
        dayClasses_list_afternoon = [formsDayClasses(request.POST,prefix=str(i)) for i in range(5,10)]
        dayClasses_list_night = [formsDayClasses(request.POST,prefix=str(i)) for i in range(10, 15)]
        

        if formClass.is_valid():
            
            if not all(form.verify_all_none() for form in dayClasses_list_morning) or not all(form.verify_all_none() for form in dayClasses_list_afternoon) or not all( form.verify_all_none() for form in dayClasses_list_night):

                formSaveClass = formClass.save()
                days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
                'Quinta-feira','Sexta-feira']

                if not all(form.verify_all_none() for form in dayClasses_list_morning) and all(form.is_valid() for form in dayClasses_list_morning):
                    for i, form in enumerate(dayClasses_list_morning):
                        form.cleaned_data['timeTable'] =  "Matutino"
                        form.instance.classObj = formSaveClass
                        form.instance.day = days[i] 
                        if form.is_valid():                        
                            form.save() 

                if not all(form.verify_all_none() for form in dayClasses_list_afternoon) and all(form.is_valid() for form in dayClasses_list_afternoon):
                    for i, form in enumerate(dayClasses_list_afternoon):
                        form.cleaned_data['timeTable'] =  "Vespertino"
                        form.day = days[i]
                        # print(form.instance.day)
                        form.instance.classObj = formSaveClass

                        if form.instance.first and dayCla.objects.filter(day=form.instance.day, timeTable=form.instance.timeTable, first__teacher=form.instance.first.teacher).exists():
                            print("EEXXXISSTEEEE")
                            messages.error(request, "ERROR")
                        else:
                            
                            form.save()  
                            
                        
                                
                        
                if not all(form.verify_all_none() for form in dayClasses_list_night) and all(form.is_valid() for form in dayClasses_list_night):
                    for i, form in enumerate(dayClasses_list_night):
                        form.instance.timeTable =  "Noturno"
                        form.instance.classObj = formSaveClass
                        form.instance.day = days[i] 
                        if form.is_valid():
                            form.save()
                        
                return redirect('FormClass')
            else:

                dayClasses_list_morning = [formsDayClasses(prefix=str(i)) for i in range(0,5)]
                dayClasses_list_afternoon = [formsDayClasses(prefix=str(i)) for i in range(5,10)]
                dayClasses_list_night = [formsDayClasses(prefix=str(i)) for i in range(10, 15)]
                for i, dayClasses in enumerate(dayClasses_list_morning):
                    dayClasses.day = days[i]
                    dayClasses_list_afternoon[i].day = days[i]
                    dayClasses_list_night[i].day = days[i]


    context = {
        'formClass': formClass,
        'class_morning': dayClasses_list_morning,
        'class_afternoon': dayClasses_list_afternoon,
        'class_night': dayClasses_list_night,
        'classes':  classes,
        'days':days,
    }

    return render(request, 'formsTurma.html', context)

def subjectsClass(request, pk):
    
    turm = Class.objects.get(pk=pk)
 
    dayClasses_list_morning = turm.dayclasses_set.filter(timeTable="Matutino")
    dayClasses_list_afternoon = turm.dayclasses_set.filter(timeTable="Vespertino")
    dayClasses_list_night = turm.dayclasses_set.filter(timeTable="Noturno")

    context = {
        'class_morning': dayClasses_list_morning,
        'class_afternoon': dayClasses_list_afternoon,
        'class_night': dayClasses_list_night,
        "turm":turm,
        
    }

    return render (request, "aulasTurma.html", context)

def subjectsTeacher(request, pk):

    dayss = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
                'Quinta-feira','Sexta-feira']
    
    teacher = Teacher.objects.get(pk=pk)
    
    
    return render (request, "aulasProfessor.html", {"teacher":teacher, "dayss": dayss})

def absentsTeachers(request):
    
    return render (request, "professoresAusentes.html")

        
