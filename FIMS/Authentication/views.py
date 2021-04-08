from django.shortcuts import render,HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.utils.datastructures import MultiValueDictKeyError
import math,random,socket
from django.core.mail import send_mail
import pyrebase
import datetime
from numpy import random

# Database Connection.
config = {
    'apiKey': "AIzaSyB0E9kvv4N7TKM6jiBeUnaUhHro8ML1UzA",
    'authDomain': "facultyinformationsystem-49a2b.firebaseapp.com",
    'projectId': "facultyinformationsystem-49a2b",
    'storageBucket': "facultyinformationsystem-49a2b.appspot.com",
    'messagingSenderId': "90902353716",
    'appId': "1:90902353716:web:44b655ed0b6a9bcd2df761",
    'measurementId': "G-RLK92EMYC8",
    'databaseURL':"https://facultyinformationsystem-49a2b-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
firbase_auth = firebase.auth()
database = firebase.database()

# Create your views here.

def SignUp(request):
    if request.method=='POST':
        username2 = request.POST['Id']
        password2 = request.POST['Password']
        try:
            user = firbase_auth.sign_in_with_email_and_password(username2,password2)
            request.session['emailid'] = username2
        except:
            messages.error(request,'invalid username or password')
            return render(request,'auth-sign-in.html')
        user_id = user['localId']
        job = database.child("users").child(user_id).child("user_details").child("job").get().val()
        college_id = database.child("users").child(user_id).child("user_details").child("collegeid").get().val()
        fname = database.child("users").child(user_id).child("user_details").child("firstname").get().val()
        session_id = user['idToken']
        request.session['uid']=str(session_id)
        request.session['user_id'] = user_id
        request.session['collegeid'] = college_id
        request.session['fname'] = fname
        user_detail = database.child("users").child(user_id).child("user_details").get().val()
        request.session['userdetails'] = user_detail
        if(job == "Admin"):
            return redirect('/Admin/')
        else:
            return redirect('/Faculty/')
    return render(request,'auth-sign-in.html')

def RecoverPassword(request):
    return render(request,'auth-recoverpw.html')


def signout(request):
    try:
        del request.session['uid']
    except:
        pass    
    messages.success(request,'Succesfully Signed-Out')
    return redirect('/')



    