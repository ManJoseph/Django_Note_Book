import datetime
import uuid
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxLengthValidator, MinLengthValidator

class UserManager(BaseUserManager):

    def create_user(self, email, username, first_name, password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not first_name:
            raise ValueError("First name is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, password):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.email



class Note(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def create_note(self, title, content):
        note = Note(title=title, content=content)
        note.save()
        return note
    
    def update_note(self, title, content):
        self.title = title
        self.content = content
        self.save(using=self._db)
        return self

    def delete_note(self):
        self.delete()
        return self
