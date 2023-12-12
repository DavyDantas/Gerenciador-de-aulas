from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Teacher, Subject, categoryCourse
from .models import dayClasses as dayC
from .forms import *
from django.contrib import messages

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

            
            if not all(form.verify_all_none() for form in dayClasses_list_morning):
                print('testes manhã')
                if not all(form.is_valid() for form in dayClasses_list_morning):
                    
                    save_all = False
                    dayClasses_list_morning = [formsDayClasses(request.POST, prefix=str(i)) for i in range(0,5)]
                
            if not all(form.verify_all_none() for form in dayClasses_list_afternoon):
                print('testes tarde')
                if not all(form.is_valid() for form in dayClasses_list_afternoon):
                    
                    save_all = False
                    dayClasses_list_afternoon = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5,10)]

            if not all(form.verify_all_none() for form in dayClasses_list_night):
                print('testes noite')
                if not all(form.is_valid() for form in dayClasses_list_night):
                
                    save_all = False
                    dayClasses_list_night = [formsDayClasses(request.POST, prefix=str(i)) for i in range(10,15)]

            if save_all:
                formClass.save()
                if not all(form.verify_all_none() for form in dayClasses_list_morning):[form.save() for form in dayClasses_list_morning]
                if not all(form.verify_all_none() for form in dayClasses_list_afternoon):[form.save() for form in dayClasses_list_afternoon]
                if not all(form.verify_all_none() for form in dayClasses_list_night):[form.save() for form in dayClasses_list_night]
                return redirect('FormClass')

        else:

            dayClasses_list_morning = [formsDayClasses(request.POST, prefix=str(i)) for i in range(0,5)]
            dayClasses_list_afternoon = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5,10)]
            dayClasses_list_night = [formsDayClasses(request.POST, prefix=str(i)) for i in range(10, 15)]
            
            for i, dayClasse in enumerate(dayClasses_list_morning):
                for field in ['first','second','third','fourth','fifth','sixth']:
                    dayClasse.fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Matutino').values(field)))
                    dayClasses_list_afternoon[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Vespertino').values(field)))
                    dayClasses_list_night[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Noturno').values(field))) 



    context = {
        'formClass': formClass,
        'class_morning': dayClasses_list_morning,
        'class_afternoon': dayClasses_list_afternoon,
        'class_night': dayClasses_list_night,
        'classes':  Class.objects.all(),
        'days':days,
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

    dayss = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
                'Quinta-feira','Sexta-feira']
    
    teacher = Teacher.objects.get(pk=pk)
    
    
    return render (request, "Teacher/aulasProfessor.html", {"teacher":teacher, "dayss": dayss})

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
        form = formsSubject(instance=subject, initial=subject.clean())

    return render(request, "Subject/editDisciplina.html", {"form":form, "subject":subject})

def subjectDelete(request, pk):

    if request.method == "GET":
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()

    return redirect("FormSubject")




def classEdit(request, pk):
    
    clas = get_object_or_404(Class,pk=pk)
    dayClass_morning = dayClasses.objects.filter(classObj = clas, timeTable = "Matutino")
    dayClass_afternoon = dayClasses.objects.filter(classObj = clas, timeTable = "Vespertino")
    dayClass_night = dayClasses.objects.filter(classObj = clas, timeTable = "Noturno")
    days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
            'Quinta-feira','Sexta-feira']
    save_all=True


    if request.method == "POST":
        form = formsClass(request.POST, instance=clas)
        dayClass_morning_form = [formsDayClasses(request.POST, instance=item) for item in dayClass_morning]
        dayClass_afternoon_form = [formsDayClasses(request.POST, instance=item) for item in dayClass_afternoon]
        dayClass_night_form = [formsDayClasses(request.POST, instance=item) for item in dayClass_night]

        for i, dayClasse in enumerate(dayClass_morning_form):
            for field in ['first','second','third','fourth','fifth','sixth']:
                dayClasse.fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Matutino').values(field)))
                dayClass_afternoon_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Vespertino').values(field)))
                dayClass_night_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Noturno').values(field))) 


        if form.is_valid():

            if not all(form.verify_all_none() for form in dayClass_morning_form):
                print('testes manhã')
                if not all(form.is_valid() for form in dayClass_morning_form):
                    
                    save_all = False
                    dayClass_morning_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(0,5)]
                
            if not all(form.verify_all_none() for form in dayClass_afternoon_form):
                print('testes tarde')
                if not all(form.is_valid() for form in dayClass_afternoon_form):
                    
                    save_all = False
                    dayClass_afternoon_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(5,10)]

            if not all(form.verify_all_none() for form in dayClass_night_form):
                print('testes noite')
                if not all(form.is_valid() for form in dayClass_night_form):
                
                    save_all = False
                    dayClass_night_form = [formsDayClasses(request.POST, prefix=str(i)) for i in range(10,15)]

            if save_all:
                form.save()
                if not all(form.verify_all_none() for form in dayClass_morning_form):[form.save() for form in dayClass_morning_form]
                if not all(form.verify_all_none() for form in dayClass_afternoon_form):[form.save() for form in dayClass_afternoon_form]
                if not all(form.verify_all_none() for form in dayClass_night_form):[form.save() for form in dayClass_night_form]
                return redirect('FormClass')

    else:
        dayClass_morning_form = [formsDayClasses(instance=dayClass_morning)]
        dayClass_afternoon_form = [formsDayClasses(instance=dayClass_afternoon)]
        dayClass_night_form = [formsDayClasses(instance=dayClass_night)]
        
        for i, dayClasse in enumerate(dayClass_morning_form):
            for field in ['first','second','third','fourth','fifth','sixth']:
                dayClasse.fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Matutino').values(field)))
                dayClass_afternoon_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Vespertino').values(field)))
                dayClass_night_form[i].fields[field].queryset = Subject.objects.exclude(teacher__in = Teacher.objects.filter(subject__in = dayC.objects.filter(dayWeek = days[i], timeTable = 'Noturno').values(field))) 



    context = {
        'formClass': form,
        'class_morning': dayClass_morning_form,
        'class_afternoon': dayClass_afternoon_form,
        'class_night': dayClass_night_form,    
        'class': clas,
    }

    return render(request, "Class/formsTurma.html", context)