from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from datetime import date
from django.db.models import Q

class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, error_messages={'unique': 'Этот email уже зарегестрирован'})
    username = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=16)

    USERNAME_FIELD = 'username'

    objects = UserManager()
        
    def check_user_exists(self, login):
        try:
            user = User.objects.get(Q(email=login) | Q(username=login))
            return True
        except User.DoesNotExist:
            return False

    def __str__(self):
        return self.email