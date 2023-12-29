from django.urls import path, re_path
from .views import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', login_view, name="login"),
    path('logout', login_required(logout_view), name="logout"),
    path('editar-usuario', login_required(userEdit), name="UserEdit"),
    path('editar-senha', login_required(changePassword), name="PasswordEdit"),
    re_path(r'^$', lambda x: redirect('index'), name='index'),
    path('lista-turmas', login_required(listarTurmas), name="index"),
    path('form-turmas', login_required(classForm), name="FormClass"),
    path('editar-turma/<int:pk>', login_required(classEdit), name="ClassEdit"),
    path('excluir-turma/<int:pk>', login_required(classDelete), name="ClassDelete"),
    path('aulas-Turma/<int:pk>', login_required(subjectsClass), name="SubjectsClass"),
    path('lista-Professores', login_required(listarProfessores), name="listarProfessores"),
    path('form-Professores', login_required(teacherForm), name="FormTeacher"),
    path('editar-professor/<int:pk>', login_required(teacherEdit), name = 'EditTeacher' ),
    path('excluir-professor/<int:pk>', login_required(teacherDelete), name='teacherDelete'),
    path('aulas-Professor/<int:pk>', login_required(subjectsTeacher), name="SubjectsTeacher"),
    path('form-Disciplinas', login_required(subjectForm), name="FormSubject"),
    path('editar-Disciplina/<int:pk>', login_required(subjectEdit), name="SubjectEdit"),
    path('excluir-Disciplina/<int:pk>', login_required(subjectDelete), name="SubjectDelete"),
    path('form-Cursos', login_required(courseForm), name="FormCourse"),
    path('editar-Curso/<int:pk>', login_required(courseEdit), name="CourseEdit"),
    path('excluir-Curso/<int:pk>', login_required(courseDelete), name="CourseDelete"),
    path('Professores-Ausentes', login_required(absentsTeachers), name="AbsentsTeachers"),
    path('excluir-ausencia/<int:pk>', login_required(absentDelete), name="absentDelete"),
]
