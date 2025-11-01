from django.shortcuts import render,redirect
from .models import Enquiry,LoginInfo,UserInfo
from django.contrib import messages
from adminapp.models import *

# Create your views here.

def index(request):
    books=Book.objects.all()
    return render(request,'index.html',{'books':books})


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':  
        name=request.POST.get('name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        enq=Enquiry(name=name,email=email, contact=contact,subject=subject,message=message)
        enq.save()
        messages.success(request, 'your message has been submitted successfully')
        return redirect('contact')
    return render(request, 'contact.html')


def adminlogin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            ad=LoginInfo.objects.get(usertype='admin',username=username,password=password)
            if ad is not None:
                request.session['adminid']=username
                messages.success(request, 'admin login Successfully')
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, 'Invalid username and password') 
            return redirect('adminlogin')
        
    return render(request, 'adminlogin.html')

def register(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password != cpassword:
            messages.error(request, 'Password and Confirm Password does not match')
            return redirect('register')
        ch=LoginInfo.objects.filter(username=email)
        if ch:
            messages.error(request, 'Email already exists')
            return redirect('register')
        log=LoginInfo(usertype='user',username=email,password=password)
        user=UserInfo(name=name,email=email,contact=contact,login=log)
        log.save()
        user.save()
        messages.success(request, 'Registered Successfully')
        return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            ul=LoginInfo.objects.get(usertype='user',username=username,password=password)
            if ul is not None:
                request.session['userid']=username
                messages.success(request, ' login Successfully')
                return redirect('userdash')
        except LoginInfo.DoesNotExist:
            messages.error(request, 'Invalid username and password') 
            return redirect('login')
        
    return render(request, 'login.html')

def book_details(request,id):
    book=Book.objects.get(id=id)
    return render(request,'book_details.html',{'book':book})
