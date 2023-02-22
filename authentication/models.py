from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django import forms
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        admin_list = UserType.objects.filter(name="ADMIN")
        admin = admin_list.first()
        if not admin_list.exists():
            admin = UserType()
            admin.name = "ADMIN"
            admin.is_active = True
            admin.description = "Admin"
            admin.save()
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", admin)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class UserType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = "user_type"


class CustomUser(AbstractUser):
    user_type = models.ForeignKey(UserType, models.CASCADE, null=False, blank=False)

    objects = UserManager()

    class Meta:
        db_table = "user"


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class LogoutForm(forms.Form):
    username = forms.EmailField(required=True)
