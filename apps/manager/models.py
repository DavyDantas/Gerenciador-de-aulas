from django.db import models
from django.core.files.storage import default_storage
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from sgra.users.models import User
# Create your models here.

class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numberAbsents = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.user.name
    
class categoryCourse(models.Model):

    name = models.CharField(max_length=150, blank=False)
    periods = models.IntegerField()
    coordinator = models.OneToOneField(Teacher, on_delete=models.SET_NULL,null=True, unique=True, error_messages={'unique': "Este professor já é coordenador de um curso"})

    def __str__(self) :
        return self.name
    

class Class(models.Model):

    PERIOD_CHOICES = (
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno'),
    )

    course = models.ForeignKey(categoryCourse, on_delete=models.CASCADE)
    timeTable = models.CharField(max_length=15, choices=PERIOD_CHOICES)
    period = models.IntegerField()
    acronym = models.CharField(max_length=10, unique=True, error_messages={'unique': "Já existe uma turma com está abreviação"})

    def __str__(self) :
        return self.acronym
    
class Subject(models.Model):

    name = models.CharField(max_length=150)
    acronym = models.CharField(max_length=10, unique=True, error_messages={'unique': "Já existe uma disciplina com está abreviação"})
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True) 

    def __str__(self) :
        return self.name
    
class dayClasses(models.Model):

    timeTable = models.CharField(max_length=15)
    classObj = models.ForeignKey(Class, on_delete=models.CASCADE) 
    dayWeek = models.CharField(max_length=50)
    first = models.ForeignKey(Subject, related_name="first", on_delete=models.SET_NULL, null=True, blank=True)
    second = models.ForeignKey(Subject, related_name="second", on_delete=models.SET_NULL, null=True, blank=True)
    third = models.ForeignKey(Subject, related_name="third", on_delete=models.SET_NULL, null=True, blank=True)
    fourth = models.ForeignKey(Subject, related_name="fourth", on_delete=models.SET_NULL, null=True, blank=True)
    fifth = models.ForeignKey(Subject, related_name="fifth", on_delete=models.SET_NULL, null=True, blank=True)
    sixth = models.ForeignKey(Subject, related_name="sixth", on_delete=models.SET_NULL, null=True, blank=True)

class Absent(models.Model):

    PERIOD_CHOICES = (
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno'),
    )

    CLASS_CHOICES = [
        ('1','1º'),
        ('2','2º'),
        ('3','3º'),
        ('4','4º'),
        ('5','5º'),
        ('6','6º'),
    ]

    absentTeacher = models.ForeignKey(Teacher, related_name="absentTeacher", on_delete=models.CASCADE)
    substituteTeacher = models.ForeignKey(Teacher, related_name="substituteTeacher", on_delete=models.SET_NULL, null=True, blank=True)
    classObj = models.ForeignKey(Class, on_delete=models.CASCADE)
    timeTable = models.CharField(max_length=15, choices=PERIOD_CHOICES)
    absentClass = models.CharField(max_length=15, choices=CLASS_CHOICES, blank=False)
    absentDate = models.DateField() 

    def clean(self):
        clean_data = super().clean()
        value = " ".join(clean_data['absentClass'])
        clean_data['absentClass'] = value
        print("32423",clean_data)
        return clean_data