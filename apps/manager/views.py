from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Teacher, Subject, categoryCourse
from .models import dayClasses as dayC
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from sgra.users.forms import *
import re
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .decorators import group_required
from django.contrib.auth.forms import AuthenticationForm
import datetime
# Create your views here.

def login_view(request):
    message = ""

    if request.method == "GET":
        form = AuthenticationForm()
    
    else:
        form = AuthenticationForm(request, request.POST)
        
        if form.is_valid():
            print("valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                print("usuario invalido")
                message = "Matrícula ou senha inválida"
        else:
            message = "Matrícula ou senha inválida"

    return render(request, "login.html", {'form': form, 'message':message})

def logout_view(request):
    logout(request)
    return redirect("login")

def listarProfessores(request):
    teachers = Teacher.objects.all()
    return render(request,'Teacher/listaProfessores.html', {'teachers':teachers})
 
def listarTurmas(request):
    
    courses = categoryCourse.objects.all()
    context = {'courses':courses}

    return render(request, "Class/listaTurmas.html", context)

@group_required(["GERENTE"])
def teacherForm(request):
    teachers = Teacher.objects.all()
    
    if request.method == "GET":
        form = UserSignupForm()
        
    else:
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Teacher.objects.create(user=user)
            return redirect('FormTeacher')

    context={
        'form': form,
        'teachers': teachers,
        }
    return render(request, "Teacher/formsProfessor.html", context)

def userEdit(request):
    
    if request.method == "GET":
        form_user = EditUser(instance=request.user)
       
    else:
        value = request.POST.copy()
        value["username"] = request.user.username
        form_user = EditUser(value, request.FILES, instance=request.user)

        print(form_user)
        if form_user.is_valid():
            form_user.save()

            return redirect('index')

    context={
        'form_user': form_user,
        }
    return render(request, "editUser.html", context)

def changePassword(request):

    if request.method == "GET":
        form_password = PasswordChangeForm(request.user)
    else:
        form_password = PasswordChangeForm(request.user, request.POST)
        
        if form_password.is_valid():
            form_password.save()
            return redirect('index')

    context={
        'form_password': form_password,
        }
    return render(request, "editPassword.html", context)

@group_required(["GERENTE"])
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

@group_required(["GERENTE"])
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
    return render(request, "Course/formsCurso.html", context)

@group_required(["GERENTE"])
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
    
    turm = get_object_or_404(Class, pk=pk)
    absents = turm.absent_set.all()
    teacher = None

    if request.user.groups.filter(name="PROFESSOR").exists():
        teacher = get_object_or_404(Teacher, pk=request.user.teacher.pk)

    dayClasses_list_morning = turm.dayclasses_set.filter(timeTable="Matutino")
    dayClasses_list_afternoon = turm.dayclasses_set.filter(timeTable="Vespertino")
    dayClasses_list_night = turm.dayclasses_set.filter(timeTable="Noturno")

    formAbsent = formsAbsent()

    if request.method == "POST":
        data = request.POST.copy()
        data["classObj"] = turm 

        if teacher:
            data["absentTeacher"] = teacher

        formAbsent = formsAbsent(data)
        if formAbsent.is_valid():
            form_model = formAbsent.save()
            absentTeacher = get_object_or_404(Teacher, pk=form_model.absentTeacher.pk)
            absentTeacher.numberAbsents += len(re.findall(r'\d+', form_model.absentClass))
            absentTeacher.save()

            return redirect("SubjectsClass", pk=pk)

    context = {
        'class_morning': dayClasses_list_morning,
        'class_afternoon': dayClasses_list_afternoon,
        'class_night': dayClasses_list_night,
        "turm":turm,
        'form': formAbsent,
        'absents' : absents,
        'teacher': teacher,
    }

    return render (request, "Class/aulasTurma.html", context)


def subjectsTeacher(request, pk):

    days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira','Sexta-feira']
    fields = ['first','second','third','fourth','fifth','sixth']

    teacher = Teacher.objects.get(pk=pk)
    form = formsTeacher()
    dayClass_morning_list = []
    dayClass_afternoon_list = []
    dayClass_night_list = []

    for day in days:
        dayClass_morning = []
        dayClass_afternoon = []
        dayClass_night = []

        for field in fields:

            query = dayClasses.objects.filter(**{f"{field}__teacher": teacher}, timeTable = "Matutino", dayWeek = day)
            if query: 
                subject_instance = get_object_or_404(dayClasses, pk=query.first().pk)
                dayClass_morning.append(subject_instance)
            else:
                dayClass_morning.append([])

            query = dayClasses.objects.filter(**{f"{field}__teacher": teacher}, timeTable = "Vespertino", dayWeek = day)
            if query: 
                subject_instance = get_object_or_404(dayClasses, pk=query.first().pk)
                dayClass_afternoon.append(subject_instance)
            else:
                dayClass_afternoon.append([]) 

            query = dayClasses.objects.filter(**{f"{field}__teacher": teacher}, timeTable = "Noturno", dayWeek = day)
            if query: 
                subject_instance = get_object_or_404(dayClasses, pk=query.first().pk)
                dayClass_night.append(subject_instance)
            else:
                dayClass_night.append([])

        dayClass_morning_list.append(dayClass_morning)
        dayClass_afternoon_list.append(dayClass_afternoon)
        dayClass_night_list.append(dayClass_night)
        
    if all(data==[] for vetor in dayClass_morning_list for data in vetor):
        dayClass_morning_list = []
    if all(data==[] for vetor in dayClass_afternoon_list for data in vetor):
        dayClass_afternoon_list = []
    if all(data==[] for vetor in dayClass_night_list for data in vetor):
        dayClass_night_list = []

    print(dayClass_morning_list)
    print(dayClass_afternoon_list)

    if request.method == "POST":
        form = formsTeacher(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("SubjectsTeacher", pk=pk)

    context = {
        'class_morning': dayClass_morning_list,
        'class_afternoon': dayClass_afternoon_list,
        'class_night': dayClass_night_list,
        "teacher":teacher, 
        "dayss": days,
        'form': form
    }

    return render (request, "Teacher/aulasProfessor.html", context)

def absentsTeachers(request):
    
    absents = Absent.objects.all()
    teachers_list = [value.absentTeacher for value in absents]
    turms_list = [value.classObj for value in absents]
    substitutes_list = [value.substituteTeacher for value in absents]
    schedule_list = [value.absentClass for value in absents] 
    timeTable_list = [value.timeTable for value in absents]
    if request.user.groups.filter(name="PROFESSOR").exists():
        teacher = get_object_or_404(Teacher, pk=request.user.teacher.pk)
    else:
        teacher = None
    form_list = [formsAbsent(instance=absent, prefix=i, initial=absent.clean()) for i, absent in enumerate(absents)]
    absents_list = [get_object_or_404(Absent, pk=value.pk) for value in absents]

    if request.method == "POST":
        prefix = request.POST.get('form-prefix', 'default_prefix')

        data_post = request.POST.copy()
        if int(prefix) != 0: 
            date = str(data_post[prefix+"-absentDate"]).split("-")
            value_date = datetime.date(int(date[0]), int(date[1]), int(date[2])) 
            data_post[prefix+"-absentDate"] = value_date
            data_post[prefix+"-absentTeacher"] = absents_list[int(prefix)].absentTeacher 
        else:
            date = str(data_post["absentDate"]).split("-")
            value_date = datetime.date(int(date[0]), int(date[1]), int(date[2])) 
            data_post["absentDate"] = value_date
            data_post["absentTeacher"] = absents_list[int(prefix)].absentTeacher 

        form = formsAbsent(data_post, instance=absents[int(prefix)], prefix=prefix)
        print(form) 
        if form.is_valid():
            print("valido")
            form_value = form.save()
            if form.cleaned_data["substituteTeacher"] and teacher != form.cleaned_data["absentTeacher"]:
                absentTeacher = get_object_or_404(Teacher, pk=form_value.substituteTeacher.pk)
                absentTeacher.numberAbsents -= len(re.findall(r"\d+", form_value.absentClass))
                absentTeacher.save()
 
            return redirect("AbsentsTeachers")


    context ={
        'teacher': teacher,
        'form_list' : form_list,
        'teachers_list': teachers_list,
        'turms_list': turms_list,
        'timeTable_list': timeTable_list,
        'substitutes_list': substitutes_list,
        'absents': absents_list,
        'schedule_list': schedule_list
    }

    return render (request, "Teacher/professoresAusentes.html", context=context)

def absentDelete(request, pk):

    absent = get_object_or_404(Absent, pk=pk)
    teacher = get_object_or_404(Teacher, pk=absent.absentTeacher.pk)
    teacher.numberAbsents -= len(re.findall(r'\d+', absent.absentClass))
    teacher.save()
    absent.delete()

    return redirect("AbsentsTeachers")

@group_required(["GERENTE"])
def teacherEdit(request, pk):

    teacher = get_object_or_404(User, pk=pk)
    
    if request.method == "POST":
        form = EditUser(request.POST,request.FILES, instance = teacher)

        if form.is_valid():
            form.save()
            return redirect('FormTeacher')

    else:
        form = EditUser(instance=teacher, initial=teacher.clean())

    return render(request, "Teacher/editProfessor.html", {"form":form, "teacher":teacher})

@group_required(["GERENTE"])
def teacherDelete(request, pk):
    
    teacher = get_object_or_404(User, pk=pk)
   
    if request.method == "GET":
        teacher.delete()
    
    return redirect("FormTeacher")

@group_required(["GERENTE"])
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

@group_required(["GERENTE"])
def courseDelete(request, pk):

    if request.method == "GET":
        course = get_object_or_404(categoryCourse, pk=pk)
        course.delete()

    return redirect("FormCourse")

@group_required(["GERENTE"])
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

@group_required(["GERENTE"])
def subjectDelete(request, pk):

    if request.method == "GET":
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()

    return redirect("FormSubject")

@group_required(["GERENTE"])
def classEdit(request, pk):
    
    clas = get_object_or_404(Class,pk=pk)
    dayClasses_morning_list = []
    dayClasses_afternoon_list = []
    dayClasses_night_list = []
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
            else: 
                dayClass_morning_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(0,5)]
                for index in range(5):
                    dayClass_morning_form[index].instance.dayWeek = days[index]
                    dayClass_morning_form[index].instance.timeTable = "Matutino"
                    dayClass_morning_form[index].instance.classObj = class_save
            dayClasses_morning_list.extend(dayClass_morning_form) 
            dayClasses_list.extend(dayClass_morning_form) 

            if dayClass_afternoon: 
                dayClass_afternoon_form = [formsDayClasses(request.POST, instance= item, prefix=str(i+5)) for i, item in enumerate(dayClass_afternoon)]
            else: 
                dayClass_afternoon_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5,10)]
                for index in range(5):
                    dayClass_afternoon_form[index].instance.dayWeek = days[index]
                    dayClass_afternoon_form[index].instance.timeTable = "Vespertino"
                    dayClass_afternoon_form[index].instance.classObj = class_save    
            dayClasses_afternoon_list.extend(dayClass_afternoon_form)
            dayClasses_list.extend(dayClass_afternoon_form) 
            
            if dayClass_night: 
                dayClass_night_form = [formsDayClasses(request.POST, instance=item, prefix=str(i+10)) for i, item in enumerate(dayClass_night)]
            else: 
                dayClass_night_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(10,15)]
                for index in range(5):
                    dayClass_night_form[index].instance.dayWeek = days[index]
                    dayClass_night_form[index].instance.timeTable = "Noturno"
                    dayClass_night_form[index].instance.classObj = class_save
            dayClasses_night_list.extend(dayClass_night_form) 
            dayClasses_list.extend(dayClass_night_form) 

            if not all(form.verify_all_none() for form in dayClasses_list):

                if all(form.is_valid() for form in dayClasses_list):
                    formClass.save()
                    if not all(form.verify_all_none() for form in dayClasses_morning_list):[form.save() for form in dayClasses_morning_list]
                    if not all(form.verify_all_none() for form in dayClasses_afternoon_list):[form.save() for form in dayClasses_afternoon_list]
                    if not all(form.verify_all_none() for form in dayClasses_night_list):[form.save() for form in dayClasses_night_list]
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

@group_required(["GERENTE"])
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