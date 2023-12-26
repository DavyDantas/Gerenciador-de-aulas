from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget

class formsTeacher(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["numberAbsents"]
        widgets = {
            'numberAbsents': forms.NumberInput(attrs={'class': 'form-element '}),
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
        if all(value == None for value in self.cleaned_data.values()):
            return True


    # def clean(self):
    #     timeTable = self.instance.timeTable
    #     days = self.instance.dayWeek 

    #     for field in self.fields:    
    #         data = self.cleaned_data.get(field)
            
    #         if data :    
    #             teacher = data.teacher
    #             if dayClasses.objects.filter(dayWeek=days, timeTable=timeTable, **{f'{field}__teacher':teacher}).exists():
    #                 self.add_error(field, _("Professor está em aula neste horário"))
    #                 raise ValidationError(_("Este professor já está dando aula neste horário"))
     
    #     return self.cleaned_data

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

class formsAbsent(forms.ModelForm):

    absentClass = forms.MultipleChoiceField(choices=Absent.CLASS_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-element checkbox'}), required=True)
 
    class Meta:
        model = Absent
        fields = "__all__"
        widgets = {
        'absentTeacher' : forms.Select(attrs={'class': 'form-element-select'}),
        'substituteTeacher' : forms.Select(attrs={'class': 'form-element-select'}),
        'timeTable': forms.Select(attrs={'class': 'form-element-select horary'}),
        'classObj' : forms.Select(attrs={'class': 'form-element-select'}),
        'absentDate': forms.TextInput(attrs={'type': 'date', 'class': 'form-element', 'placeholder': 'Selecione a data'}),
        }  

class EditAbsent(forms.ModelForm):
    class Meta:
        model = Absent
        fields = ["substituteTeacher"]
        widgets = {
        'substituteTeacher' : forms.Select(attrs={'class': 'form-element-select'}),
        } 
    
    
    # def clean(self):
    #     clean_data = super().clean()
    #     value = " ".join(clean_data['absentClass'])
    #     clean_data['absentClass'] = value
    #     print("32423",clean_data)
    #     return clean_data
             

    # def clean_absentClass(self):
    #     value = self.cleaned_data.get('absentClass')
    #     return ",".join(value) if value else ""

    # def clean(self):
        
    #     data = self.cleaned_data.get('absentClass']
    #     print(data)
    #     return [int(value) for value in data.split(',')]