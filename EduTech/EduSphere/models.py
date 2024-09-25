from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course')

#Create models for assignments and quizzes to track students' progress:
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_on = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(null=True, blank=True)

class CustomUserManager(UserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_admin= models.BooleanField('Is admin', default=False)
    is_instructor = models.BooleanField('Is Instructor', default=False)
    is_student = models.BooleanField('Is Learner', default=True)
    is_userid = models.UUIDField('User ID',default=uuid.uuid4, editable=False, unique=True)
    #phone_number = models.PhoneNumberField(region='NG', unique=True, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
    
class bio(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)
    surname = models.CharField(max_length=500)
    middle_name = models.CharField(max_length=500)
    first_name = models.CharField(max_length=500)
    gender = models.CharField(max_length=20)