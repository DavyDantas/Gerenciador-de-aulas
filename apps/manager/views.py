from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Teacher, Subject, categoryCourse
from .models import dayClasses as dayC
from .forms import *
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def Login(request):

    return render(request, "login.html")

def listarProfessores(request):
    teachers = Teacher.objects.all()
    return render(request,'Teacher/listaProfessores.html', {'teachers':teachers})

def listarTurmas(request):
    
    courses = categoryCourse.objects.all()
    context = {'courses':courses}

    return render(request, "Class/listaTurmas.html", context)

def teacherForm(request):
    teachers = Teacher.objects.all()
    
    if request.method == "GET":
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
    return render(request, "Teacher/formsProfessor.html", context)

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
    return render(request, "Subject/formsDisciplina.html", context)

def courseForm(request):

    courses = categoryCourse.objects.all()
    if request.method == "GET":
        form = formsCourse()
        
    
    else:
        form = formsCourse(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Course/FormCourse')

    context={
        'form': form,
        'courses': courses,
        }
    return render(request, "Course/formsCurso.html", context)

def classForm(request):
    
    save_all = True
    error_dayClasses_none = None
    days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
            'Quinta-feira','Sexta-feira']

    if request.method == "GET":
        
        formClass = formsClass()
        dayClasses_list_morning = [formsDayClasses(prefix=str(i)) for i in range(0,5)]
        dayClasses_list_afternoon = [formsDayClasses(prefix=str(i)) for i in range(5,10)]
        dayClasses_list_night = [formsDayClasses(prefix=str(i)) for i in range(10, 15)]

        for i, dayClasse in enumerate(dayClasses_list_morning):
            for field in ['first','second','third','fourth','fifth','sixth']:
                dayClasse.fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Matutino').values(field)))
                dayClasses_list_afternoon[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Vespertino').values(field)))
                dayClasses_list_night[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Noturno').values(field))) 
                
    else:
        
        formClass = formsClass(request.POST)
        dayClasses_list_morning = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5)] 
        dayClasses_list_afternoon = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5,10)]
        dayClasses_list_night = [formsDayClasses(request.POST,prefix=str(i)) for i in range(10, 15)]
        
        if formClass.is_valid():
        
            formSaveClass = formClass.save(commit=False)

            for index in range(5):

                    dayClasses_list_morning[index].instance.classObj = formSaveClass
                    dayClasses_list_morning[index].instance.dayWeek = days[index]
                    dayClasses_list_morning[index].instance.timeTable = "Matutino"

                    dayClasses_list_afternoon[index].instance.classObj = formSaveClass
                    dayClasses_list_afternoon[index].instance.dayWeek = days[index]
                    dayClasses_list_afternoon[index].instance.timeTable = "Vespertino"

                    dayClasses_list_night[index].instance.classObj = formSaveClass
                    dayClasses_list_night[index].instance.dayWeek = days[index]
                    dayClasses_list_night[index].instance.timeTable = "Noturno"

            if not all(form.verify_all_none() for form in dayClasses_list_morning) or  not all(form.verify_all_none() for form in dayClasses_list_afternoon) or not all(form.verify_all_none() for form in dayClasses_list_night):

                if not all(form.verify_all_none() for form in dayClasses_list_morning):
                    print('testes manhã')
                    if not all(form.is_valid() for form in dayClasses_list_morning):
                        save_all = False

                if not all(form.verify_all_none() for form in dayClasses_list_afternoon):
                    print('testes tarde')
                    if not all(form.is_valid() for form in dayClasses_list_afternoon):
                        save_all = False

                if not all(form.verify_all_none() for form in dayClasses_list_night):
                    print('testes noite')
                    if not all(form.is_valid() for form in dayClasses_list_night):
                        save_all = False

                if save_all:
                    formClass.save()
                    if not all(form.verify_all_none() for form in dayClasses_list_morning):[form.save() for form in dayClasses_list_morning]
                    if not all(form.verify_all_none() for form in dayClasses_list_afternoon):[form.save() for form in dayClasses_list_afternoon]
                    if not all(form.verify_all_none() for form in dayClasses_list_night):[form.save() for form in dayClasses_list_night]
                    return redirect('FormClass')

            else:
                error_dayClasses_none = "Nenhum horario adicionado a turma"

        dayClasses_list_morning = [formsDayClasses(request.POST, prefix=str(i)) for i in range(0,5)]
        dayClasses_list_afternoon = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5,10)]
        dayClasses_list_night = [formsDayClasses(request.POST, prefix=str(i)) for i in range(10, 15)]

    context = {
        'formClass': formClass,
        'class_morning': dayClasses_list_morning,
        'class_afternoon': dayClasses_list_afternoon,
        'class_night': dayClasses_list_night,
        'classes':  Class.objects.all(),
        'days':days,
        'error_dayClasses_none':error_dayClasses_none,
    }

    return render(request, 'Class/formsTurma.html', context)

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

    return render (request, "Class/aulasTurma.html", context)

def subjectsTeacher(request, pk):

    days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira','Sexta-feira']
    fields = ['first','second','third','fourth','fifth','sixth']

    teacher = Teacher.objects.get(pk=pk)
    dayClass_morning_list = []

    for day in days:
        dayClass_morning = dayClasses()
        for field in fields:

            query = dayClasses.objects.filter(**{f"{field}__teacher": teacher}, timeTable = "Matutino", dayWeek = day)
            subject_instance = get_object_or_404(Subject, pk=query.values("first").first().get("first"))
            setattr(dayClass_morning, field, subject_instance)

        dayClass_morning_list.append(dayClass_morning)
    
    dayClass_afternoon = dayClasses.objects.filter(Q(first__teacher=teacher) |
    Q(second__teacher=teacher) |
    Q(third__teacher=teacher) |
    Q(fourth__teacher=teacher) |
    Q(fifth__teacher=teacher) |
    Q(sixth__teacher=teacher), timeTable = "Vespertino")

    dayClass_night = dayClasses.objects.filter(Q(first__teacher=teacher) |
    Q(second__teacher=teacher) |
    Q(third__teacher=teacher) |
    Q(fourth__teacher=teacher) |
    Q(fifth__teacher=teacher) |
    Q(sixth__teacher=teacher), timeTable = "Noturno")

    print("TARDE:",dayClass_afternoon,"\n")
    print("MANHÃ:",dayClass_morning_list,"\n")
    print("NOITE:",dayClass_night,"\n")

    context = {
        'class_morning': dayClass_morning_list,
        'class_afternoon': dayClass_afternoon,
        'class_night': dayClass_night,
        "teacher":teacher, 
        "dayss": days
        
    }

    return render (request, "Teacher/aulasProfessor.html", context)

def absentsTeachers(request):
    
    return render (request, "Teacher/professoresAusentes.html")

def teacherEdit(request, pk):

    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == "POST":
        form = formsTeacher(request.POST,request.FILES, instance=teacher)

        if form.is_valid():
            form.save()
            return redirect('FormTeacher')

    else:
        form = formsTeacher(instance=teacher, initial=teacher.clean())

    return render(request, "Teacher/editProfessor.html", {"form":form, "teacher":teacher})

def teacherDelete(request, pk):
    
    teacher = get_object_or_404(Teacher, pk=pk)
   
    if request.method == "GET":
        teacher.delete()
    
    return redirect("FormTeacher")

def courseEdit(request, pk):

    course = get_object_or_404(categoryCourse,pk=pk)

    if request.method == "POST":
        form = formsCourse(request.POST, instance=course)
        if form.is_valid():
            form.save()

            return redirect("FormCourse")
        
    else:
        form = formsCourse(instance=course, initial=course.clean())

    return render(request, "Course/editCursos.html", {"form":form, "course":course})

def courseDelete(request, pk):

    if request.method == "GET":
        course = get_object_or_404(categoryCourse, pk=pk)
        course.delete()

    return redirect("FormCourse")

def subjectEdit(request, pk):
    
    subject = get_object_or_404(Subject,pk=pk)

    if request.method == "POST":
        form = formsSubject(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("FormSubject")
        
    else:
        form = formsSubject(instance=subject)

    return render(request, "Subject/editDisciplina.html", {"form":form, "subject":subject})

def subjectDelete(request, pk):

    if request.method == "GET":
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()

    return redirect("FormSubject")

def classEdit(request, pk):
    
    clas = get_object_or_404(Class,pk=pk)
    dayClasses_list = []
    dayClass_morning = dayClasses.objects.filter(classObj = clas, timeTable = "Matutino")
    dayClass_afternoon = dayClasses.objects.filter(classObj = clas, timeTable = "Vespertino")
    dayClass_night = dayClasses.objects.filter(classObj = clas, timeTable = "Noturno")
    days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
            'Quinta-feira','Sexta-feira']
    error_dayClasses_none = None

    if request.method == "POST":

        formClass = formsClass(request.POST, instance=clas, prefix="class")
        if formClass.is_valid():
            class_save = formClass.save(commit=False)

            if dayClass_morning: 
                dayClass_morning_form = [formsDayClasses(request.POST, instance=item, prefix=str(i)) for i, item in enumerate(dayClass_morning)]
                print("tem manhã")
            else: 
                print(" não tem manhã")
                dayClass_morning_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(0,5)]
                for index in range(5):
                    dayClass_morning_form[index].instance.dayWeek = days[index]
                    dayClass_morning_form[index].instance.timeTable = "Matutino"
                    dayClass_morning_form[index].instance.classObj = class_save
            dayClasses_list.extend(dayClass_morning_form) 
            print( dayClasses_list,"\n")
            if dayClass_afternoon: 
                dayClass_afternoon_form = [formsDayClasses(request.POST, instance= item, prefix=str(i+5)) for i, item in enumerate(dayClass_afternoon)]
            else: 
                dayClass_afternoon_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5,10)]
                for index in range(5):
                    dayClass_afternoon_form[index].instance.dayWeek = days[index]
                    dayClass_afternoon_form[index].instance.timeTable = "Vespertino"
                    dayClass_afternoon_form[index].instance.classObj = class_save    
            dayClasses_list.extend(dayClass_afternoon_form)
            print( dayClasses_list,"\n")
            
            if dayClass_night: 
                dayClass_night_form = [formsDayClasses(request.POST, instance=item, prefix=str(i+10)) for i, item in enumerate(dayClass_night)]
            else: 
                dayClass_night_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(10,15)]
                for index in range(5):
                    dayClass_night_form[index].instance.dayWeek = days[index]
                    dayClass_night_form[index].instance.timeTable = "Noturno"
                    dayClass_night_form[index].instance.classObj = class_save
            dayClasses_list.extend(dayClass_night_form) 
            print( dayClasses_list,"\n")
            if not all(form.verify_all_none() for form in dayClasses_list):
                print("passou2")
                if all(form.is_valid() for form in dayClasses_list):
                    print("passo3")
                    formClass.save()
                    for form in dayClasses_list:
                        
                        form.save()
                    return redirect('FormClass')
                
                else:
                    error_dayClasses_none = "Horários invalidos"
            else:
                error_dayClasses_none="Formulário inválido ou nenhuma disciplina adicionada a turma"
    else:
        formClass = formsClass(instance=clas, prefix="class")
        if dayClass_morning:
            dayClass_morning_form = [formsDayClasses(instance=item, prefix=str(i)) for i, item in enumerate(dayClass_morning)]
        else: 
            dayClass_morning_form = [formsDayClasses(prefix=str(i)) for i in range(0,5)]
        if dayClass_afternoon:
            dayClass_afternoon_form = [formsDayClasses(instance=item, prefix=str(i+5)) for i, item in enumerate(dayClass_afternoon)]
        else:
            dayClass_afternoon_form = [formsDayClasses(prefix=str(i)) for i in range(5,10)]
        if dayClass_night:
            dayClass_night_form = [formsDayClasses(instance=item, prefix=str(i+10)) for i, item in enumerate(dayClass_night)]
        else:
            dayClass_night_form = [formsDayClasses(prefix=(str(i))) for i in range(10, 15)]

    for i in range(5):
        for field in ['first','second','third','fourth','fifth','sixth']:
            
            if dayClass_morning and getattr(dayClass_morning[i], field):
                dayClass_morning_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Matutino').values(field))).union(Subject.objects.filter(teacher = getattr(dayClass_morning[i], field).teacher))
            else:
                dayClass_morning_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Matutino').values(field)))
            if dayClass_afternoon and getattr(dayClass_afternoon[i], field):
                dayClass_afternoon_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Vespertino').values(field))).union(Subject.objects.filter(teacher = getattr(dayClass_afternoon[i], field).teacher))
            else:
                dayClass_afternoon_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Vespertino').values(field)))
            if dayClass_night and getattr(dayClass_night[i], field):
                dayClass_night_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Noturno').values(field))).union(Subject.objects.filter(teacher = getattr(dayClass_night[i], field).teacher))
            else:
                dayClass_night_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Noturno').values(field))) 

    print(dayClass_morning_form)

    context = {
        'formClass': formClass,
        'class_morning': dayClass_morning_form,
        'class_afternoon': dayClass_afternoon_form,
        'class_night': dayClass_night_form,    
        'class': clas,
        'error_dayClasses_none': error_dayClasses_none,
        'days':days,
    }

    return render(request, "Class/editClass.html", context)

def classDelete(request, pk):

    if request.method == "GET":
        clas = get_object_or_404(Class,pk=pk)
        dayClass_morning = dayClasses.objects.filter(classObj = clas, timeTable = "Matutino")
        dayClass_afternoon = dayClasses.objects.filter(classObj = clas, timeTable = "Vespertino")
        dayClass_night = dayClasses.objects.filter(classObj = clas, timeTable = "Noturno")

        clas.delete()
        for index in range(5):
            if dayClass_morning:
                dayClass_morning[index].delete()
            if dayClass_afternoon:
                dayClass_afternoon[index].delete()
            if dayClass_night:
                dayClass_night[index].delete()
        
        return redirect("FormClass")