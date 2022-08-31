import re
from telnetlib import LOGOUT
from unittest import result
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import  User 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from authentication.models import Courses
from gomate import settings
from django.core.mail import send_mail
import random

#import authentication
# Create your views here

def home(request):
    return render(request,'authentication/home.html',{})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username):
            messages.error(request,'Username already exists.')
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,'Already a user registered using this Email.')
            return redirect('home')

        if len(username)>10:
            messages.error(request,'Username Must be under 10 characters.')
            return redirect('home')

        if not username.isalnum():
            messages.error(request,'Username must be alpha-Numeric.')
            return redirect('home')

        myuser = User.objects.create_user(username,email,password)
        otp = random.randint(100000,999999)
        myuser.first_name = fname
        #myuser.otp = otp
        myuser.save()
        messages.success(request,"Your Account has been created successfully. Check Email for OTP verification.")
        
        #Welcome Email
        subject = "Verification!!!"
        msg = f"Hello  {myuser.first_name}, Thank You for Visiting Us. You verfication code: {otp}"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,msg,from_email,to_list,fail_silently=True)
        return redirect('signin')
    return render(request, 'authentication/signup.html',{})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user != None:
            login(request,user)
            fname = user.first_name
            email = user.email
            return render(request, 'authentication/home.html',{'fname':fname,'username':username,'email':email})
        else:
            messages.error(request,'Bad credentials')
            return redirect('home')
    else:
        return render(request, 'authentication/signin.html',{})

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def homeforUser(request):
    return render(request,'authentication/homeforUser.html')
'''firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
mydatabase = firebase.database'''
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        result = Courses.objects.filter(name__contains=searched)
        return render(request, 'authentication/search.html',
            {'searched':searched,
            'Courses': result})
    else:
        return render(request, 'authentication/search.html',
            {})

def payment(request):
    return render(request, 'authentication/payment.html',{})
def user(request):
    #malik = User.objects.filter(username=username)
    return render(request, 'authentication/user.html',{})
def course_list(request):
    result = Courses.objects.all()
    return render(request, 'authentication/course_list.html',
    {'Courses': result})
def course_page(request):
    result = Courses.objects.all()
    return render(request, 'authentication/course_page.html',
    {'Courses': result})
