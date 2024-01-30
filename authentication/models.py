from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
      raise ValueError('Users must have an email address')
    email = self.normalize_email(email)
    user = self.model(
      email=email,
      is_staff=is_staff,
      is_superuser=is_superuser,
      **extra_fields
    )
    user.set_password(password)
    user.save()
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    return self._create_user(email, password, True, True, True, **extra_fields)

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    