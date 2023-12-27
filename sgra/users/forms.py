from typing import Any
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSignupForm(UserCreationForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-element'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-element'}))
    imgProfileVariable = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-element hidden'}), required=False)
    telephone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-element'}))

    def clean(self):
        cleaned_data = super().clean()
        username = str(cleaned_data.get('username'))
        name = cleaned_data["name"]
        name = name.split(" ")
        # Verificar se a matrícula está presente antes de definir as senhas
        if username:
            cleaned_data['password1'] = name[0] + name[1] + username
            cleaned_data['password2'] = name[0] + name[1] + username

        print(cleaned_data)

        return cleaned_data

    class Meta:
        model = User
        fields = ['name', 'username', 'imgProfileVariable', 'telephone']

class EditUser(forms.ModelForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-element'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-element'}))
    imgProfileVariable = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-element hidden'}), required=False)
    telephone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-element'}))
 

    class Meta:
        model = User
        fields = ['name', 'username', 'imgProfileVariable', 'telephone']
class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
