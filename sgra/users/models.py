from collections.abc import Iterable
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.files.storage import default_storage

class User(AbstractUser):
    """
    Default custom user model for SGRA.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=False, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    matriculation = models.IntegerField(unique=True, error_messages={'unique': "Matrícula já cadastrada"})
    imgProfileVariable = models.ImageField(blank=True, default="user-profile-icon.jpg", upload_to="UsersProfile/")
    telephone = models.CharField(blank=True, null=True, default = None)

    USERNAME_FIELD = "matriculation"  # ele usa por padrão o username
    REQUIRED_FIELDS = ['name'] 


    def __str__(self) :
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        self.username = str(self.matriculation)
        super().save(*args, **kwargs)

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
