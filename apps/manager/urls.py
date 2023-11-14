from django.urls import path
from .views import *

urlpatterns = [
    path('', Login, name="login"),
    path('lista-Professores', listarProfessores, name="listarProfessores"),
    path('lista-Turmas', listarTurmas, name="listarTurmas"),
    path('form-Professores', teacherForm, name="FormTeacher"),
    path('editar-professor/<int:pk>', teacherEdit, name = 'EditTeacher' ),
    path('form-Disciplinas', subjectForm, name="FormSubject"),
    path('form-Turmas', classForm, name="FormClass"),
    path('form-Cursos', courseForm, name="FormCourse"),
    path('aulas-Turma/<int:pk>', subjectsClass, name="SubjectsClass"),
    path('aulas-Professor/<int:pk>', subjectsTeacher, name="SubjectsTeacher"),
    path('Professores-Ausentes', absentsTeachers, name="AbsentsTeachers"),
]