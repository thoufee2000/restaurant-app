from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import Dish


# Create your views here.

def home(request):
    return render(request, 'home.html')


def menu(request):
    d = Dish.objects.filter(available=True)
    return render(request, 'menu.html', {'dish': d})


def register(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        fn = request.POST['fn']
        ln = request.POST['ln']
        e = request.POST['e']

        if cp == p:
            u = User.objects.create_user(username=u, password=p, first_name=fn, last_name=ln, email=e)
            u.save()
            return redirect('shop:home')
        else:
            messages.error(request, 'Passwords are not same')
    return render(request, 'register.html')


def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']

        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:home')
        else:
            messages.error(request,'Entered Credentials does not match')
    return render(request, 'login.html')
@login_required
def user_logout(request):
    logout(request)
    return home(request)

def search_menu(request):
    d=None
    s=''
    if(request.method=="POST"):
        s=request.POST['s']
        if s:
            d=Dish.objects.filter(name__icontains=s)
    return render(request,'search.html',{'dishes':d,'search':s})
