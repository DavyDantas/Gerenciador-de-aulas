from django.urls import path
from .views import *

urlpatterns = [
    path('lista-professores', listarProfessores, name="listarProfessores"),
    path('', listarTurmas, name="listarTurmas"),
    path('form-Professores', teacherForm, name="FormTeacher"),
    path('form-Disciplinas', subjectForm, name="FormSubject"),
    path('form-Turmas', classForm, name="FormClass"),
]