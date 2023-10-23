from django.db import models

# Create your models here.

class Teacher(models.Model):

    name = models.CharField(max_length=200)
    matriculation = models.IntegerField()
    imgProfile = models.ImageField(default="user-profile-icon.jpg", upload_to="UsersProfile/")

    def __str__(self) :
        return self.name
    
class categoryCourse(models.Model):

    name = models.CharField(max_length=150, blank=False)

    def __str__(self) :
        return self.name
    

class Class(models.Model):

    PERIOD_CHOICES = (
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno'),
    )

    name = models.CharField(max_length=150, blank=False)
    acronym = models.CharField(max_length=10)
    course = models.ForeignKey(categoryCourse, on_delete=models.CASCADE)
    timeTable = models.CharField(max_length=15, choices=PERIOD_CHOICES)
    period = models.IntegerField()

    def __str__(self) :
        return self.name
    
class Subject(models.Model):

    name = models.CharField(max_length=150)
    acronym = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self) :
        return self.name
    
class dayClasses(models.Model):
    classObj = models.ForeignKey(Class, on_delete=models.CASCADE) 
    day = models.CharField(max_length=50)
    first = models.ForeignKey(Subject, related_name="first", on_delete=models.SET_NULL, null=True, blank=True)
    second = models.ForeignKey(Subject, related_name="second", on_delete=models.SET_NULL, null=True, blank=True)
    third = models.ForeignKey(Subject, related_name="third", on_delete=models.SET_NULL, null=True, blank=True)
    fourth = models.ForeignKey(Subject, related_name="fourth", on_delete=models.SET_NULL, null=True, blank=True)
    fifth = models.ForeignKey(Subject, related_name="fifth", on_delete=models.SET_NULL, null=True, blank=True)
    sixth = models.ForeignKey(Subject, related_name="sixth", on_delete=models.SET_NULL, null=True, blank=True)

    
