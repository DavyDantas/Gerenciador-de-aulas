from django.db import models

# Create your models here.

class Teacher(models.Model):

    name = models.CharField(max_length=200)
    matriculation = models.IntegerField(unique=True)
    imgProfile = models.ImageField(default="user-profile-icon.jpg", upload_to="UsersProfile/")
    telefone = models.IntegerField()
    numberAbsents = models.IntegerField(null=True, blank=True, default=0)


    def __str__(self) :
        return self.name
    
class categoryCourse(models.Model):

    name = models.CharField(max_length=150, blank=False)
    periods = models.IntegerField()
    coordinator = models.OneToOneField(Teacher, on_delete=models.SET_NULL, null=True)

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
    acronym = models.CharField(max_length=10, unique=True, error_messages={'unique':"Já existe uma turma com está abreviação"})

    def __str__(self) :
        return self.acronym
    
class Subject(models.Model):

    name = models.CharField(max_length=150)
    acronym = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

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


