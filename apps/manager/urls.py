from django.urls import path
from .views import *

urlpatterns = [
    path('', Login, name="login"),
    path('lista-Turmas', listarTurmas, name="listarTurmas"),
    path('form-Turmas', classForm, name="FormClass"),
    path('edita-turma/<int:pk>', classEdit, name="ClassEdit"),
    path('aulas-Turma/<int:pk>', subjectsClass, name="SubjectsClass"),
    path('lista-Professores', listarProfessores, name="listarProfessores"),
    path('form-Professores', teacherForm, name="FormTeacher"),
    path('editar-professor/<int:pk>', teacherEdit, name = 'EditTeacher' ),
    path('excluir-professor/<int:pk>', teacherDelete, name='teacherDelete'),
    path('form-Disciplinas', subjectForm, name="FormSubject"),
    path('editar-Disciplina/<int:pk>', subjectEdit, name="SubjectEdit"),
    path('excluir-Disciplina/<int:pk>', subjectDelete, name="SubjectDelete"),
    path('form-Cursos', courseForm, name="FormCourse"),
    path('editar-Curso/<int:pk>', courseEdit, name="CourseEdit"),
    path('excluir-Curso/<int:pk>', courseDelete, name="CourseDelete"),
    path('aulas-Professor/<int:pk>', subjectsTeacher, name="SubjectsTeacher"),
    path('Professores-Ausentes', absentsTeachers, name="AbsentsTeachers"),
]