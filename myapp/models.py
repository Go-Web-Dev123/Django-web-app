from django.db import  models

# Create your models here.


class Employee(models.Model):
    fullname=models.CharField(max_length=100)
    Password=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)
    image=models.FileField(default="defaults.jpg",max_length=255)

class doctors(models.Model):
    username=models.CharField(max_length=100,default="doctor")
    Password=models.CharField(max_length=50,default="1234")

class prescription(models.Model):
    username=models.CharField(max_length=255)
    mobile=models.CharField(max_length=100)
    prescription=models.TextField()

class admin(models.Model):
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=50)
