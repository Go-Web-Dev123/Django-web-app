from django.http import request
from django.http.response import HttpResponse
from .forms import EmployeeForm,ImageForm
from django.shortcuts import render,redirect
from .models import Employee, doctors ,prescription
from django.core.files.storage import FileSystemStorage
from django.contrib import messages



# Create your views here.


def register(request):
    if request.method ==  "GET":
        form = EmployeeForm()
        return render(request,'employee_form.html',{'form':form})
    else:
     pass1=request.POST['Password']
     pass2=request.POST['password1']
     mobile=request.POST['mobile']
     context=Employee.objects.filter(mobile=mobile).exists()
     if(context==False):
        if(pass1==pass2):
         request.session['fullname']=request.POST['fullname']
         request.session['mobile']=request.POST['mobile']
         form = EmployeeForm(request.POST)
         if form.is_valid():
            form.save()
         return redirect('login/')
        else:
            messages.error(request,"Passwords doesn't Match!")
            return redirect('/')
     else:
         messages.error(request,'Mobile Number already Registered!')
         return redirect('/')





def login(request):
    return render(request,'login.html')





def logout(request):
    try:
        del request.session['fullname']
        del request.session['mobile']
        del request.session['password']
    except:
        return render(request,'login.html')
    return render(request,'login.html')



def profile(request):
    request.session['mobile']=request.POST['mobile']
    request.session['password']=request.POST['password']
    context=Employee.objects.filter(mobile=request.session['mobile'],Password=request.session['password']).exists()
    if(context==True):
        if(request.session['mobile']!=None):
           details = {'employee_list':Employee.objects.filter(mobile=request.session['mobile'],Password=request.session['password'])} 
           user = Employee.objects.all().filter(mobile=request.session['mobile'],Password=request.session['password']).first()
           if(user==None):
            return redirect('/login')
           else:
            return render(request,'employee_list.html',details)
        else:
             return redirect('/login')
    else:
         messages.error(request,'Mobile Number or Password is incorrect')
         return redirect('/login')



def image_view(request):
    if(request.session['mobile']!=None):
      if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            Employee.objects.all().filter(mobile=request.session['mobile']).update(image=img_obj.image)
            return render(request, 'index1.html', {'form': form, 'img_obj': img_obj})
      else:
        form = ImageForm()
      return render(request, 'index1.html', {'form': form})
    else:
        return redirect('/login')




def image_upload_view(request):
    """Process images uploaded by users"""
    if(request.session['mobile']!=None):
      if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            Employee.objects.all().filter(mobile=request.session['mobile']).update(image=img_obj.image)
            return render(request, 'index1.html', {'form': form, 'img_obj': img_obj})
      else:
        form = ImageForm()
      return render(request, 'index1.html', {'form': form})
    else:
        return redirect('/login')




def profiles(request):
    if(request.session['mobile']!=None):
           details = {'employee_list':Employee.objects.filter(mobile=request.session['mobile'],Password=request.session['password'])} 
           user = Employee.objects.all().filter(mobile=request.session['mobile'],Password=request.session['password']).first()
           if(user==None):
            return redirect('/login')
           else:
            return render(request,'employee_list.html',details)
    else:
             return redirect('/login')




def myprofile(request):
    if(request.session['mobile']!=None):
           details = {'employee_list':Employee.objects.filter(mobile=request.session['mobile'],Password=request.session['password'])} 
           user = Employee.objects.all().filter(mobile=request.session['mobile'],Password=request.session['password']).first()
           if(user==None):
            return redirect('/login')
           else:
            return render(request,'employee_list1.html',details)
    else:
             return redirect('/login')