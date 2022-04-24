from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

       
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, name, email, dob, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(name, email, dob, password, **other_fields)

    def create_user(self, name, email, dob, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(name=name, email=email, dob=dob, **other_fields)
        user.set_password(password)
        user.save()
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    dob = models.DateField(verbose_name='Date of Birth')
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(auto_now= True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'dob']

    def __str__(self):
        return self.email