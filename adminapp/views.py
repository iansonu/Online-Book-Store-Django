from django.shortcuts import render,redirect
from django.contrib import messages
from newapp.models import *
from .models import *

# Create your views here.

def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,'please login first')
        return redirect('adminlogin')
    return render(request, 'admindash.html')

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session ['adminid']
        messages.success(request, 'Admin Logout Successfully')
        return redirect('adminlogin')
    else:
        messages.error(request,'please login first!')
        return redirect('index')
    
def viewenquiry(request):
    if not 'adminid' in request.session:
        messages.error(request,'please login first')
        return redirect('adminlogin')
    enqs=Enquiry.objects.all()
    return render(request,'viewenquiry.html',{'enqs':enqs})


def delenquiry(request,id):
    if not 'adminid' in request.session:
        messages.error(request,'please login first')
        return redirect('adminlogin')
    try:
        enq=Enquiry.objects.get(id=id)
        enq.delete()
        messages.success(request,'Enquiry Deleted Successfully')
        return redirect('viewenquiry')
    except Enquiry.DoesNotExist:
        messages.error(request,'Enquiry Not found!')
        return redirect('viewenquiry')

def adminchangepwd(request):
    if not 'adminid' in request.session:
        messages.error(request,'please login first')
        return redirect('adminlogin')
    adminid=request.session['adminid']
    if request.method=='POST':
        oldpwd=request.POST.get('oldpwd')
        newpwd=request.POST.get('newpwd')
        cpwd=request.POST.get('cpwd')
        try:
            admin=LoginInfo.objects.get(username=adminid)
            if admin.password!=oldpwd:
                messages.error(request, 'Old Password Not Match!')
                return redirect('adminchangepwd')
            elif newpwd!=cpwd:
                messages.error(request,'New Password and Confirm Password Not Be same')
                return redirect('adminchangepwd')
            else:
                admin.password=newpwd
                admin.save()
                messages.success(request,'Password Change Successfully')
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,'something Went Wrong')
            return redirect('adminchangepwd')
    return render(request,'adminchangepwd.html')

def addcat(request):
    if not 'adminid' in request.session:
        messages.error(request,'please login first!')
        return redirect('adminlogin')
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        cat=Category(name=name,description=description)
        cat.save()
        messages.success(request,'Category Added Successfully')
        return redirect('addcat')
    return render(request, 'addcat.html')

def viewcat(request):
    if not 'adminid' in request.session:
        messages.error(request,'please Login First!')
        return redirect('adminlogin')
    cats=Category.objects.all()
    return render(request,'viewcat.html',{'cats':cats})

def addbook(request):
    if not 'adminid' in request.session:
        messages.error(request,'please login first!')
        return redirect('adminlogin')
    cats=Category.objects.all()
    if request.method =='POST':
        title=request.POST.get('title')
        author=request.POST.get('author')
        catid=request.POST.get('category')
        cat=Category.objects.get(id=catid)
        description=request.POST.get('description')
        original_price=request.POST.get('original_price')
        price=request.POST.get('price')
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        book=Book(title=title,author=author,category=cat,description=description,original_price=original_price,price=price,published_date=published_date,language=language,cover_image=cover_image,stock=stock)
        book.save()
        messages.success(request,'Book Added Successfully')
        return redirect('addbook')
        
    return render(request,'addbook.html',{'cats':cats}) 



def viewbook(request):
    if not 'adminid' in request.session:
        messages.error(request,'Please login first!')
        return redirect('adminlogin')
    books=Book.objects.all()
    return render(request,'viewbook.html',{'books':books})
