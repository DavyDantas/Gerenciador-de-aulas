from django.shortcuts import render, redirect
from .models import *
from .forms import *

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

def classForm(request):

    classes = Class.objects.all()

    if request.method == "GET":

        days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
                'Quinta-feira','Sexta-feira']
        formClass = formsClass()

        
        dayClasses_list_morning = [formsDayClasses(prefix=str(i)) for i in range(0,5)]
        dayClasses_list_afternoon = [formsDayClasses(prefix=str(i)) for i in range(5,10)]
        dayClasses_list_night = [formsDayClasses(prefix=str(i)) for i in range(10, 15)]
        for i, dayClasses in enumerate(dayClasses_list_morning):
            dayClasses.day = days[i]
            dayClasses_list_afternoon[i].day = days[i]
            dayClasses_list_night[i].day = days[i]
                


    else:
        days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
                'Quinta-feira','Sexta-feira']
        formClass = formsClass(request.POST)
        dayClasses_list_morning = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5)]
        dayClasses_list_afternoon = [formsDayClasses(request.POST,prefix=str(i)) for i in range(5,10)]
        dayClasses_list_night = [formsDayClasses(request.POST,prefix=str(i)) for i in range(10, 15)]
        

        if formClass.is_valid():
            
            if not all(form.verify_all_none() for form in dayClasses_list_morning) or not all(form.verify_all_none() for form in dayClasses_list_afternoon) or not all( form.verify_all_none() for form in dayClasses_list_night):
                print("dddddddddddddddddd ALGUM FORM VALIDO")
                formSaveClass = formClass.save()

                if not all(form.verify_all_none() for form in dayClasses_list_morning):
                    for i, form in enumerate(dayClasses_list_morning):
                        form.instance.timeTable =  "Matutino"
                        form.instance.classObj = formSaveClass
                        form.instance.day = days[i] 
                        form.save() 

                if not all(form.verify_all_none() for form in dayClasses_list_afternoon):
                    for i, form in enumerate(dayClasses_list_afternoon):
                        form.instance.timeTable =  "Vespertino"
                        form.instance.classObj = formSaveClass
                        form.instance.day = days[i] 
                        form.save() 
                        
                if not all(form.verify_all_none() for form in dayClasses_list_night):
                    for i, form in enumerate(dayClasses_list_night):
                        form.instance.timeTable =  "Noturno"
                        form.instance.classObj = formSaveClass
                        form.instance.day = days[i] 
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

                print("aaaaaaaaaaaaaaaaaa TODOS OS FORMS VZIOS")
    context = {
        'formClass': formClass,
        'class_morning': dayClasses_list_morning,
        'class_afternoon': dayClasses_list_afternoon,
        'class_night': dayClasses_list_night,
        'classes':  classes,
    }

    return render(request, 'formsTurma.html', context)

def subjectsClass(request, pk):

    turm = Class.objects.get(pk=pk)
    
    return render (request, "aulasTurma.html", {"turm":turm})

def subjectsTeacher(request, pk):

    dayss = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
                'Quinta-feira','Sexta-feira']
    
    teacher = Teacher.objects.get(pk=pk)
    
    return render (request, "aulasProfessor.html", {"teacher":teacher, "dayss": dayss})

def absentsTeachers(request):
    
    return render (request, "professoresAusentes.html")

        
