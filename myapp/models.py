from django.db import  models
from django.db.models.fields import CharField, DateField

# Create your models here.


class Employee(models.Model):
    fullname=models.CharField(max_length=100)
    Password=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)
    image=models.FileField(default="defaults.jpg",max_length=255)
    age=models.CharField(default="0",max_length=10)
    BloodGroup=models.CharField(default="0",max_length=10)
    doctor=models.CharField(max_length=50,default="Doctor")
    height=models.CharField(max_length=10,default="0cm")
    weight=models.CharField(max_length=5,default="0kg")
    address=models.CharField(max_length=255,default="0")
    checkup=models.DateField()
    gender=models.CharField(default="Human",max_length=255)
    BP=models.CharField(max_length=255,default="Not Yet")
    glucose=models.CharField(max_length=255,default="Not Yet")
    sugar=models.CharField(max_length=255,default="No")
    email=models.CharField(max_length=255,default="email")
    healthissue=models.CharField(max_length=255,default="Patient")




class doctors(models.Model):
    username=models.CharField(max_length=100,default="doctor")
    Password=models.CharField(max_length=50,default="1234")
    email=models.CharField(max_length=255,default="balahari765@gmail.com")
    qualification=models.CharField(max_length=255,default="Not Yet")
    specialization=models.CharField(max_length=255,default="Not Yet")
    hospital=models.CharField(max_length=255,default="Hospital")
    image=models.FileField(default='defaults.jpg')




class prescription(models.Model):
    usernames=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    date=models.DateField(auto_now=True)
    doctor=models.CharField(max_length=255,default="Doctor")
    prescription=models.TextField(default="Not Yet Added")
    image=models.FileField(default='defaults.jpg')


class advise(models.Model):
    username=models.CharField(max_length=255)
    mobile=models.CharField(max_length=10)
    date=models.DateField(auto_now=True)
    advise=models.TextField(default="Not Yet Added")

class manager(models.Model):
    username=models.CharField(max_length=255)
    email=models.CharField(default="balahari765@gmail.com",max_length=255)
    password=models.CharField(max_length=50)