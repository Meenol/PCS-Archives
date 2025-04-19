from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name
    
class Site(models.Model):
    siteid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Entity(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Site, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='entitypfp/', default='entitypfp/default_image.png')  # Changed to ImageField
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE)
    description = models.TextField(default="No description provided.")

    def __str__(self):
        return self.name
    


class SecurityClearance(models.Model):
    scid = models.AutoField(primary_key=True)
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.level


class Personnel(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    clearance = models.ForeignKey(SecurityClearance, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    clearance = models.ForeignKey('SecurityClearance', on_delete=models.SET_NULL, null=True)
    quote = models.CharField(max_length=100, default="Silenced.")
    image = models.ImageField(upload_to='userpfp/', default='userpfp/default_image.png')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def __str__(self):
        return self.username

