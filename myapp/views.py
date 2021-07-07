from django import http
from django.db.models.manager import Manager
from django.db.models.query import ModelIterable
from django.http import request
from django.http.response import HttpResponse
from .forms import ImageForm
from django.shortcuts import render,redirect
from .models import Employee, advise, doctors, prescription,manager
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    return render(request,'about.html')

def forgotpass(request):
    return render(request,'base.html')

def changepassword(request):
    return render(request,'changepassword.html')

def forgotpasssent(request):
        if request.method == 'POST':
            mail=request.POST['email']
            request.session['email']=request.POST['email']
            context=Employee.objects.filter(email=mail).exists()
            if(context==True):
                send_mail(
                    subject='Click the link to get redirected to ',
                    message = 'http://127.0.0.1:8000/changepassword/',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[request.POST['email']],
                    fail_silently=False
                )
                messages.success(request,"Recovery Email has been sent to your Email ID")
                return redirect("/forgotpassword/")
            else:
                messages.error(request,"Sorry! It is not a registered Email Id")
                return redirect("/forgotpassword/")
        else:
            return HttpResponse('NO')

def changedpassword(request):
    if request.method == "POST":
        new=request.POST['new']   
        email=request.session['email'] 
        Employee.objects.filter(email=request.session['email']).update(Password=new)
        return redirect('/login/')

def login(request):
    return render(request,'login.html')


def updatepass(request,id):
    context={'employee':Employee.objects.filter(id=id)}
    return render(request,'updatepass.html',context)


def updatedpass(request,id):
    if request.method == "POST":
        old=request.POST['old']
        new=request.POST['new']
        context={'employee':Employee.objects.filter(id=id)}
        contexts=Employee.objects.all().filter(id=id,Password=old).exists()
        if(contexts==True):
            Employee.objects.all().filter(id=id,Password=old).update(Password=new)
            return render(request,'updatepass1.html',context)
        else:
            messages.error(request,'Old Password Error')
            return render(request,'updatepass.html',context)



def logout(request):
    try:
        del request.session['fullname']
        del request.session['mobile']
        del request.session['password']
        del request.session['email']
    except:
        return render(request,'login.html')
    return render(request,'login.html')



def profile(request):
    request.session['mobile']=request.POST['mobile']
    request.session['password']=request.POST['password']
    context=Employee.objects.filter(mobile=request.session['mobile'],Password=request.session['password']).exists()
    if(context==True):
        if(request.session['mobile']!=None):
           details = {'employee_list':Employee.objects.filter(mobile=request.session['mobile'],Password=request.session['password']),'employee':advise.objects.all().filter(mobile=request.session['mobile'])} 
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
           details = {'employee_list':Employee.objects.filter(mobile=request.session['mobile'],Password=request.session['password'])} 
           user = Employee.objects.all().filter(mobile=request.session['mobile'],Password=request.session['password']).first()
           if(user==None):
            return redirect('/login')
           else:
            return render(request,'employee_list.html',details)





def myprofile(request):
           details = {'employee_list':Employee.objects.filter(mobile=request.session['mobile']),'employee':advise.objects.all().filter(mobile=request.session['mobile']) }
           user = Employee.objects.all().filter(mobile=request.session['mobile']).first()
           if(user==None):
            return redirect('/login')
           else:
            return render(request,'employee_list1.html',details)





def myprofiles(request,id):
    if(request.session['mobile']!=None):
     details = {'employee_list':Employee.objects.filter(id=id),'employee':advise.objects.all().filter(mobile=request.session['mobile']) }
     return render(request,'employee_list1.html',details)
    else:
        return redirect('/logout/')






def doctor(request):
    return render(request,'doctorlogin.html')





def doctorlogin(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        request.session['username']=request.POST['username']
        request.session['password']=request.POST['password']
        context=doctors.objects.all().filter(username=username,Password=password).exists()
        if(context==True):
           profile={'doctor':Employee.objects.filter(doctor=username),'patients':doctors.objects.filter(username=username,Password=password)}
           return render(request,'doctorprofile.html',profile)
        else:
             messages.error(request,'Username or Password Error')
             return redirect('/doctor/login/')








def addprescription(request,id):
    if(request.session['username']!=None):
     profile={'prescription':Employee.objects.filter(id=id)}
     return render(request,'addprescription.html',profile)
    else:
        return redirect('/doctor/logout/')


def myprescription(request):
    if(request.session['username']!=None):
        doctor=request.session['username']
        context={'pres':prescription.objects.filter(doctor=doctor)}
        return render(request,'myprescription.html',context)
    else:
        return redirect('/doctor/logout/')





def addedprescription(request,id):
    if(request.session['username']!=None):
        if request.method == "POST":
            name=request.POST['username']
            doctor=request.session['username']
            mobile=request.POST['mobile']
            prescriptions=request.POST['prescription']
            image=request.FILES['image']
            prescription.objects.create(usernames=name,mobile=mobile,prescription=prescriptions,doctor=doctor,image=image)
            profile={'prescription':Employee.objects.filter(id=id)}
            return render(request,'addprescriptions.html',profile)

    else:
        return redirect('/doctor/logout/')






def doctorprofile(request):
    if(request.session['username']!=None): 
        profile={'doctor':Employee.objects.filter(doctor=request.session['username']),'patients':doctors.objects.filter(username=request.session['username'])}
        return render(request,'doctorprofile.html',profile)
    else:
        return redirect('/doctor/logout/')







def doclogout(request):
    try:
        del request.session['username']
    except:
        return render(request,'doctorlogin.html')
    return render(request,'doctorlogin.html')







def docpatients(request,id):
    if(request.session['username']!=None):
        profile={'prescription':Employee.objects.filter(id=id)}
        return render(request,'patientprofile.html',profile)
    else:
        return redirect('/doctor/logout/')







def admin(request):
    return render(request,'adminlogin.html')








def adminprofile(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        request.session['username']=request.POST['username']
        request.session['password']=request.POST['password']
        context=manager.objects.all().filter(username=username,password=password).exists()
        if(context==True):
           profile={'admin':manager.objects.filter(username=username,password=password)}
           return render(request,'adminprofile.html',profile)
        else:
             messages.error(request,'Username or Password Error')
             return redirect('/admin/logining/')







def adminlogout(request):
    try:
        del request.session['username']
        del request.session['password']
    except:
        return render(request,'adminlogin.html')
    return render(request,'adminlogin.html')


def docmyprofile(request,username):
    if(request.session['username']!=None):
        context={'doctor':doctors.objects.filter(username=username)}
        return render(request,'doctorprofiles.html',context)
    else:
        return redirect('/doctor/logout/')


def dochome(request):
    if(request.session['username']!=None):
        profile={'doctor':Employee.objects.filter(doctor=request.session['username']),'patients':doctors.objects.filter(username=request.session['username'])}
        return render(request,'doctorhome.html',profile)
    else:
        return redirect('/doctor/logout/')     

def docpassupdate(request):
    if(request.session['username']!=None):  
        context={'doctor':doctors.objects.filter(username=request.session['username'])}
        return render(request,'docpassupdate.html',context)
    else:
        return redirect('/doctor/logout/')

def doctorpassupdate(request):

        context={'doctor':doctors.objects.filter(username="Doctor1")}
        return render(request,'doctorpassupdate.html',context)

def docpass(request):
    if(request.session['username']!=None):
        if request.method == "POST":
            oldp=request.POST['old']
            newp=request.POST['new']
            username=request.POST['username']
            context=doctors.objects.filter(username=username,Password=oldp).exists()
            if(context):
                doctors.objects.filter(username=username,Password=oldp).update(Password=newp)
                return redirect('/doctor/myprofile/update/')
            else:
                messages.error(request,'Old Password Error')
                return redirect('/doctor/myprofile/error/')
    else:
        return redirect('/doctor/logout/')


def reports(request,fullname):    
        context={'pres':prescription.objects.all().filter(usernames=fullname,mobile=request.session['mobile'])}
        return render(request,'reports.html',context)



def addadvise(request,id):
    if(request.session['username']!=None): 
        context={'employee':Employee.objects.filter(id=id)}
        return render(request,'advise.html',context)

def addedadvise(request,id):
    if(request.session['username']!=None): 
        if request.method == "POST":
            name=request.POST['username']
            mobile=request.POST['mobile']
            pres=request.POST['prescription']
            advise.objects.create(username=name,mobile=mobile,advise=pres)
            context={'employee':Employee.objects.filter(id=id)}
            return render(request,'addedadvise.html',context)
        else:
            messages.error(request,'Some Error in Adding')
            context={'employee':Employee.objects.filter(id=id)}
            return render(request,'adviseerror.html',context)



def viewuser(request):
    if(request.session['username']!=None): 
        context={'patients':Employee.objects.all().filter()}
        return render(request,'viewuser.html',context)

def updateuser(request):
    if(request.session['username']!=None): 
        context={'patients':Employee.objects.all().filter()}
        return render(request,'updateuser.html',context)

def updateuserpage(request,id):
    if(request.session['username']!=None): 
        context={'patient':Employee.objects.filter(id=id)}
        return render(request,'updatepageuser.html',context)

def updateuserfunc(request,id):
    if(request.session['username']!=None): 
        if request.method == "POST":
            fullname=request.POST['fullname']
            mobile=request.POST['mobile']
            age=request.POST['age']
            blood=request.POST['blood']
            doctor=request.POST['doctor']
            healthissue=request.POST['health']
            Employee.objects.all().filter(id=id).update(fullname=fullname,mobile=mobile,age=age,BloodGroup=blood,doctor=doctor,healthissue=healthissue)
            context={'patients':Employee.objects.all().filter()}
            return render(request,'updateuser1.html',context)
        else:
            return HttpResponse("No")

def createuser(request):
    if(request.session['username']!=None): 
        return render(request,'createuser.html')


def createuserfunc(request):
    if(request.session['username']!=None): 
        if request.method == "POST":
            fullname=request.POST['fullname']
            mobile=request.POST['mobile']
            password=request.POST['password']
            age=request.POST['age']
            blood=request.POST['blood']
            doctor=request.POST['doctor']
            health=request.POST['healthissue']
            height=request.POST['height']
            weight=request.POST['weight']
            Address=request.POST['address']
            checkup=request.POST['checkup']
            bp=request.POST['bp']
            gender=request.POST['gender']
            glucose=request.POST['glucose']
            sugar=request.POST['sugar']
            email=request.POST['email']
            Employee.objects.create(fullname=fullname,mobile=mobile,Password=password,age=age,BloodGroup=blood,doctor=doctor,healthissue=health,height=height,weight=weight,address=Address,BP=bp,glucose=glucose,sugar=sugar,checkup=checkup,gender=gender,email=email)
            return redirect('/admin/created/')
        else:
            return redirect('/admin/patients/')
    
def createduser(request):
    if(request.session['username']!=None): 
        return render(request,'createuser1.html')



def deleteuser(request):
    if(request.session['username']!=None): 
        context={'patients':Employee.objects.all()}
        return render(request,'deleteuser.html',context)

def deletuserfunc(request,id):
    if(request.session['username']!=None): 
        Employee.objects.filter(id=id).delete()
        return redirect('/admin/deletedpatient/')

def deleteduser(request):
    if(request.session['username']!=None): 
        context={'patients':Employee.objects.all()}
        return render(request,'deleteuser1.html',context)

def viewdoc(request):
    if(request.session['username']!=None): 
        context={'doctor':doctors.objects.all().filter()}
        return render(request,'viewdoc.html',context)



def createdoctor(request):
    if(request.session['username']!=None): 
        return render(request,'createdoc.html')

def createdoctorfunc(request):
    if(request.session['username']!=None): 
        if request.method == "POST":
            name=request.POST['fullname']
            password=request.POST['password']
            qualify=request.POST['qualify']
            special=request.POST['special']
            hospital=request.POST['hospital']
            doctors.objects.create(username=name,Password=password,qualification=qualify,specialization=special,hospital=hospital)
            return redirect('/admin/createddoc/')
        else:
            return redirect('admin/doctor/')
    

def createddoctor(request):
    if(request.session['username']!=None): 
        return render(request,'createdoc1.html')

def deletedoctor(request):
    if(request.session['username']!=None): 
        context={'doctor':doctors.objects.all()}
        return render(request,'deletedoctor.html',context)

def deletedoctorfunc(request,id):
    if(request.session['username']!=None): 
        doctors.objects.filter(id=id).delete()
        return redirect('/admin/deleteddoctor/')

def deleteddoctor(request):
    if(request.session['username']!=None): 
        context={'doctor':doctors.objects.all()}
        return render(request,'deletedoctor1.html',context)

def viewadmin(request):
    if(request.session['username']!=None): 
        context={'admin':manager.objects.all().filter()}
        return render(request,'viewadmin.html',context)

def createadmin(request):
    if(request.session['username']!=None): 
        return render(request,'createadmin.html')

def createadminfunc(request):
    if(request.session['username']!=None): 
        if request.method == "POST":
            username=request.POST['fullname']
            password=request.POST['password']
            email=request.POST['email']
            manager.objects.create(username=username,password=password,email=email)
            return redirect('/admin/admincreated/')
        else:
            return redirect('/admin/admin/')


def createdadmin(request):
    if(request.session['username']!=None): 
        return render(request,'createadmin1.html')


def deleteadmin(request):
    context={'admin':manager.objects.all()}
    return render(request,'deleteadmin.html',context)

def deleteadminfunc(request,id):
    manager.objects.filter(id=id).delete()
    return redirect('/admin/deletedadmin/')

def deletedadmin(request):
    context={'admin':manager.objects.all()}
    return render(request,'deleteadmin1.html',context)

def updatedoctor(request):
    context={'doctor':doctors.objects.all()}
    return render(request,'updatedoctor.html',context)

def updatedocpage(request,id):
    context={'doctor':doctors.objects.all().filter(id=id)}
    return render(request,'updatepagedoctor.html',context)

def updatedocfunc(request,id):
    if request.method == "POST":
        name=request.POST['username']
        qualify=request.POST['qualify']
        special=request.POST['special']
        hospital=request.POST['hospital']
        doctors.objects.filter(id=id).update(username=name,qualification=qualify,specialization=special,hospital=hospital)
        context={'doctor':doctors.objects.all()}
        return redirect('/admin/updatedoctor/')
    else:
        return HttpResponse("No")

def mydoctor(request,doctor):
    context={'doctor':doctors.objects.filter(username=doctor),'patients':Employee.objects.filter(mobile=request.session['mobile'])}
    return render(request,'mydoctor.html',context)

def updatepassadmin(request):
    if request.method == "POST":
        oldp=request.POST['old']
        newp=request.POST['new']
        contexts=manager.objects.filter(username=request.session['username'],password=oldp).exists()
        if(contexts):
            manager.objects.filter(username=request.session['username']).update(password=newp)
            return  redirect('/admin/updatedpassadmin/')
        else:
            messages.error(request,'Old Password Error')
            return redirect('/admin/updatepasserror/')


def updatedpassadmin(request):
   profile={'admin':manager.objects.filter(username=request.session['username'])}
   return render(request,'adminprofile1.html',profile)

def updatepasserror(request):
   profile={'admin':manager.objects.filter(username=request.session['username'])}
   return render(request,'adminprofile2.html',profile)

def docprescription(request,username):
    profile={'advice':advise.objects.filter(username=username)}
    return render(request,'doctorprescription.html',profile)

def adminhome(request):
   profile={'admin':manager.objects.filter(username=request.session['username'])}
   return render(request,'adminprofile2.html',profile)

def adminforgotpass(request):
    return render(request,'base1.html')


def adminchangepassword(request):
    return render(request,'adminchangepassword.html')

def adminforgotpasssent(request):
        if request.method == 'POST':
            mail=request.POST['email']
            request.session['email']=request.POST['email']
            context=manager.objects.filter(email=mail).exists()
            if(context==True):
                send_mail(
                    subject='Click the link to get redirected to ',
                    message = 'http://127.0.0.1:8000/admin/changepassword/',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[request.POST['email']],
                    fail_silently=False
                )
                messages.success(request,"Recovery Email has been sent to your Email ID")
                return redirect("/forgotpassword/")
            else:
                messages.error(request,"Sorry! It is not a registered Email Id")
                return redirect("/forgotpassword/")
        else:
            return HttpResponse('NO')

def adminchangedpassword(request):
    if request.method == "POST":
        new=request.POST['new']   
        email=request.session['email'] 
        manager.objects.filter(email=request.session['email']).update(password=new)
        return redirect('/admin/logining/')


def doctorforgotpass(request):
    return render(request,'base2.html')


def doctorchangepassword(request):
    return render(request,'doctorchangepassword.html')

def doctorforgotpasssent(request):
        if request.method == 'POST':
            mail=request.POST['email']
            request.session['email']=request.POST['email']
            context=doctors.objects.filter(email=mail).exists()
            if(context==True):
                send_mail(
                    subject='Click the link to get redirected to ',
                    message = 'http://127.0.0.1:8000/doctor/changepassword/',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[request.POST['email']],
                    fail_silently=False
                )
                messages.success(request,"Recovery Email has been sent to your Email ID")
                return redirect("/forgotpassword/")
            else:
                messages.error(request,"Sorry! It is not a registered Email Id")
                return redirect("/forgotpassword/")
        else:
            return HttpResponse('NO')

def doctorchangedpassword(request):
    if request.method == "POST":
        new=request.POST['new']   
        doctors.objects.filter(email=request.session['email']).update(Password=new)
        return redirect('/doctor/login/')
