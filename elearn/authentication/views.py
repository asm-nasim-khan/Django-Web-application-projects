import re
from telnetlib import LOGOUT
from unittest import result
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import  User 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from authentication.models import Courses
from elearn import settings
from django.core.mail import send_mail
import random
'''import pyrebase

config = {
    "apiKey": "AIzaSyAxibx_J2B_3s1oqbOakK2tRL0n3NaJNms",
  "authDomain": "elearn-fdbc4.firebaseapp.com",
  "databaseURL": "https://elearn-fdbc4-default-rtdb.firebaseio.com",
  "projectId": "elearn-fdbc4",
  "storageBucket": "elearn-fdbc4.appspot.com",
  "messagingSenderId": "660711261606",
  "appId": "1:660711261606:web:c602a660113146e5a67b67",
}'''

#import authentication
# Create your views here

def home(request):
    return render(request,'authentication/home.html',{})

def signup(request):
    if request.method == 'POST':
        usertype = request.POST['member_level']
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
        myuser.typeof_user = usertype
        myuser.first_name = fname
        #myuser.otp = otp
        myuser.save()
        messages.success(request,"Your Account has been created successfully. Check Email for OTP verification.")
        
        #Welcome Email
        subject = "Welcome to E-Pathshala!!!"
        msg = f"Hello  {myuser.first_name}, Thank You for Visiting Us. You verfication OtP: {otp}"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,msg,from_email,to_list,fail_silently=True)
        return redirect('signin')
        '''check = False
        check = cal(myuser.otp)
        if check == True:
            myuser.save()
            messages.success(request,"Your Account has been verified successfully.")
            return redirect('signin')
        else:
            messages.error(request,'Wrong OTP.')
            return redirect('verification')

        #return redirect('verification')'''
    return render(request, 'authentication/signup.html',{})

''' 
    
def verification(request):
    user_otp = 0
    if request.method == 'POST':
            otp_in = request.POST.get('otp')
            if user_otp == otp_in:
                return True
            else:
                return False
'''
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
    searched = 'Beginners'
    result = Courses.objects.filter(level__contains=searched)
    return render(request, 'authentication/course_list.html',
    {'searched':searched,
    'Courses': result})
