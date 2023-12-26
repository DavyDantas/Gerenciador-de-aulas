from collections.abc import Iterable
from typing import Any
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.files.storage import default_storage

class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Default custom user model for SGRA.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    name = models.CharField(_("Name of User"), blank=False, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    #username será usando como matricula no sistema
    username = models.CharField(max_length=150, unique=True, error_messages={'unique': "Matrícula já cadastrada"})
    imgProfileVariable = models.ImageField(blank=True, default="user-profile-icon.jpg", upload_to="UsersProfile/")
    telephone = models.CharField(max_length=15, blank=True, null=True, default = None)

    # USERNAME_FIELD = "matriculation"  # ele usa por padrão o username
    REQUIRED_FIELDS = ['name'] 

    def __str__(self) :
        return self.name

    # def save(self, *args, **kwargs) -> None:
    #     self.username = str(self.matriculation)
    #     super().save(*args, **kwargs)

    @property
    def imgProfile(self):
        if default_storage.exists(self.imgProfileVariable.name):
            return self.imgProfileVariable.url
        else:
            return r"\static\images\favicons\user-profile-icon.jpg" 

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
