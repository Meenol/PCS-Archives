from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator
from django.utils import timezone
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
    image = models.ImageField(upload_to='entitypfp/', default='entitypfp/default_image.png', blank=True)  # Changed to ImageField
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE)
    description = models.TextField(default="No description provided.", blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

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


from django.utils import timezone  # add at the top if not already

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    clearance = models.ForeignKey('SecurityClearance', on_delete=models.SET_NULL, null=True)
    quote = models.CharField(max_length=100, default="Silenced.")
    image = models.ImageField(upload_to='userpfp/', default='userpfp/default_image.png')
    exp = models.IntegerField(validators=[MaxValueValidator(100)], default=0)

    # 🆕 new fields:
    date_joined = models.DateTimeField(default=timezone.now)
    entities_documented = models.IntegerField(default=0)
    bio = models.TextField(default="", blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

