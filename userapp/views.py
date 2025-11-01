from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from adminapp.models import *
from newapp.models import *  

# Create your views here.
def userdash(request):
    if not 'userid' in request.session:
        messages.error(request,'please login first')
        return redirect('login')
    return render(request, 'userdash.html')


def userlogout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request, "You have been logged out successfully")
        return redirect('login')
    else:
        messages.error(request, "Something went wrong")
        return redirect('login')


def viewcart(request):
    if not 'userid' in request.session:
        messages.error(request, "You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    ucart=Cart.objects.filter(user=user).first()
    if ucart is None:
        cart=Cart(user=user)
        cart.save()
    items= CartItem.objects.filter(cart=Cart.objects.filter(user=user).first())
    total=0
    for i in items:
        total= total + i.get_total_price()
    context = {
        'name': user.name,
        'userid':userid,
        'profile':user.profile,
        'items':items,
        'total':total
    }
    return render(request,'viewcart.html',context)


def addtocart(request,id):
    if not 'userid' in request.session:
        messages.error(request,"you Are Not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    ucart=Cart.objects.filter(user=user).first()
    if ucart is None:
        cart=Cart(user=user)
        cart.save()
    if request.method == 'POST':
        quantity= request.POST.get('quantity')
        book=Book.objects.get(id=id)
        ci=CartItem(cart=Cart.objects.filter(user=user).first(),book=book,quantity=quantity)
        ci.save()
        messages.success(request,"Book Added To Cart")
        return redirect('viewcart')
    else:
        return redirect('index')
    
def removeitem(request,id):
    if not 'userid' in request.session:
        messages.error(request,"You Are not Logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    ucart=Cart.objects.filter(user=user).first()
    book=Book.objects.get(id=id)
    CartItem.objects.filter(cart=ucart,book=book).delete()
    messages.success(request,"Book Remove from cart")
    return redirect('viewcart')

