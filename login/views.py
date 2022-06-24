from functools import cache
from multiprocessing import context
from multiprocessing.spawn import import_main_path
import profile
from typing_extensions import Self
from django.shortcuts import redirect,render
from requests import request
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import imp
from .mixins import MessaHandler
from .forms import StudentPhone,Studentotp,StudentName
from .models import Profile
import random
import uuid
# Create your views here.

def login_view(request):
    ph=StudentPhone(auto_id=True)
    if request.method=='POST':
        
        phone_number=request.POST.get('phone_number')
        # print(Profile.is_valid(phone_number=phone_number))
        if  Profile.objects.filter(phone_number=phone_number).exists():
            profile=Profile.objects.get(phone_number=phone_number)
            profile.otp=random.randint(1000,9999)
            profile.save()
            request.session['otp'] = profile.otp
            request.session['phone_number'] = phone_number
            message_handler=MessaHandler(phone_number,profile.otp).send_otp_on_phone()
            return redirect(f'/Otp')
        else:
            otp=random.randint(1000,9999)
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            message_handler=MessaHandler(phone_number,otp).send_otp_on_phone()
            return redirect(f'/Otp')
        
    return render(request,'login.html',{'form': ph})

def dashboard_view(request):
    return render(request,'dashboard.html')


def register_view(request):
    us=StudentName(auto_id=True)
    phone_number=request.session['phone_number']
    context={
        'fm': phone_number,
        'form':us
    }
    if request.method=='POST':
        username=request.POST.get('username')
        user=User.objects.create(username=username)
        profile=Profile.objects.create(user=user,phone_number=phone_number)
        return redirect(f'/dashboard')

    return render(request,'register.html',context)


# verify otp process
def otp(request):
    ot=Studentotp(auto_id=True)
    if request.method=='POST':
        otp1=request.POST.get('otp')
        otp=request.session['otp']
        phone_number=request.session['phone_number']
        print(otp)
        print(otp1)
        print(otp1==str(otp))
        if otp1==str(otp):
            if Profile.objects.filter(phone_number=phone_number).exists():
                profile=Profile.objects.get(phone_number=phone_number)
                login(request, profile.user)
                return redirect(f'/dashboard')
            else:
                return redirect(f'/register')

        return redirect(f'/Otp')

    return render(request,'Otp.html',{'form':ot})


