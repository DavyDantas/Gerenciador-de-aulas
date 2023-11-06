from django import forms
from .models import *
from django.db.models import Q

class formsTeacher(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-element'}),
            'matriculation' : forms.TextInput(attrs={'class': 'form-element'}),
            'imgProfile': forms.FileInput(attrs={'class': 'form-element', 'accept': 'image/*'}),
            'telefone': forms.NumberInput(attrs={'class': 'form-element'}),
        }

class formsSubject(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-element'}),
            'acronym' : forms.TextInput(attrs={'class': 'form-element'}),
            'teacher': forms.Select(attrs={'class': 'form-element-select'}),

        }

class formsDayClasses(forms.ModelForm):
    class Meta:
        model = dayClasses
        fields = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']
        widgets = {
            'first': forms.Select(attrs={'class': 'form-element-select'}),
            'second': forms.Select(attrs={'class': 'form-element-select'}),
            'third': forms.Select(attrs={'class': 'form-element-select'}),
            'fourth': forms.Select(attrs={'class': 'form-element-select'}),
            'fifth': forms.Select(attrs={'class': 'form-element-select'}),
            'sixth': forms.Select(attrs={'class': 'form-element-select'}),
        }

    def verify_all_none(self):
        self.is_valid()
        if all(value is None for value in self.cleaned_data.values()):
            return True

    def clean(self):
        cleaned_data = super().clean()

        for field in self.fields:
            data = cleaned_data.get(field).teacher
            day = cleaned_data.get('day')
            timeTable = cleaned_data.get('timeTable')

            if data is not None: 
                if dayClasses.objects.filter(day=day, timeTable=timeTable, 
                                        Q(first__teacher=teacher) |
                                        Q(second__teacher=teacher) |
                                        Q(third__teacher=teacher) |
                                        Q(fourth__teacher=teacher) |
                                        Q(fifth__teacher=teacher) |
                                        Q(sixth__teacher=teacher)).exists():
                    raise forms.ValidationError("Este professor já da aula neste horário")
        
        

class formsClass(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        widgets = {
        'course': forms.Select(attrs={'class': 'form-element-select'}),
        'timeTable': forms.Select(attrs={'class': 'form-element-select horary'}),
        'period': forms.NumberInput(attrs={'class': 'form-element'}),
        'acronym' : forms.TextInput(attrs={'class': 'form-element'}),
        }

class formsCourse(forms.ModelForm):
    class Meta:
        model = categoryCourse
        fields = '__all__'
        widgets = {
        'name' : forms.TextInput(attrs={'class': 'form-element'}),
        'coordinator': forms.Select(attrs={'class': 'form-element-select'}),
        'periods': forms.NumberInput(attrs={'class': 'form-element'}),
        }


