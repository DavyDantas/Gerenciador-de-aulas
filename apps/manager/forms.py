from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.day = self.instance.day
    #     self.timeTable = self.instance.timeTable

    def verify_all_none(self):
        self.is_valid()
        if all(value is None for value in self.cleaned_data.values()):
            print("none")
            return True

    def clean_first(self):
        timeTable = self.data['timeTable']
        days = self.instance.dayWeek 
        clas = self.instance.classObj
        data = self.cleaned_data.get('first')
        if data :
            
            teacher = data.teacher
            # print(self.cleaned_data)
            
            print(dayClasses.objects.filter(dayWeek=days, timeTable=timeTable))
            if dayClasses.objects.filter(dayWeek=days, timeTable=timeTable, first__teacher=teacher).exists():
                print(days, timeTable, teacher, clas)
                raise ValidationError(_("Este professor já está dando aula neste horário"))
     
        return data

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


