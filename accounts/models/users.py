from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# from .departments import Department

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("لطفا username را وارد کنید")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'مدیر سیستم'),
        ('manager', 'مدیریت'),
        ('human_resources', 'مدیر منابع انسانی'),
        ('department_manager', 'مدیر بخش'),
        ('supervisor', 'سرپرست'),
        ('employee', 'کارمند'),
    )

    username = models.CharField(max_length=45,unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='employee')
    # departman = models.ForeignKey(Department)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # برای ورود به ادمین پنل

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.username})"
    
    