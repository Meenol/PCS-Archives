from django.db import models

# Create your models here.

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name
    
class Entity(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE)

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
    location = models.CharField(max_length=100)
    clearance = models.ForeignKey(SecurityClearance, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    clearance = models.ForeignKey(SecurityClearance, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username

