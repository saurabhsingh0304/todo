from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta, date

# Create your models here.

STATUS = ((1, 'Pending'), (2, 'Completed'))


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    key = models.CharField(max_length=30, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_api_enabled = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label ):
        return True

# the title, description, category, due date

class Task(models.Model):
    task_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='taskuser')
    title = models.CharField(max_length=25, null=True, blank=True)
    description = models.CharField(max_length=75, null=True, blank=True)
    category = models.IntegerField(choices=STATUS, default=1)
    due_date = models.DateField(blank=False, null=False, default=date.today()+timedelta(days=2))
