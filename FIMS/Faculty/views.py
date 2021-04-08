from django.shortcuts import render
import pyrebase
from django.contrib import messages,auth
from django.shortcuts import render,redirect
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials
from datetime import date
import datetime
import requests
import random

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
storage = firebase.storage()
cred = credentials.Certificate("static/firebase/facultyinformationsystem-49a2b-firebase-adminsdk-zqjh4-e9e8acf30d.json")
firebaseadmin = firebase_admin.initialize_app(cred)




# Create your views here.
user_data = {}
def FacultyHome(request):
    uid = request.session['user_id']
    user = database.child("users").child(uid).child("user_details").get().val()
    global user_data
    time_table = {}
    table = database.child("Timetable").get().val()
    if table:
        for t in table:
            time_table[t] = table[t]
    for item in user:
        user_data[item] = user[item]
    notices = database.child("Notice").get()
    notice = []
    for i in notices.each():
        notice.append(i.val())
    print(notice)    
    args = {"detail":dict(request.session['userdetails']),"user":user_data,"notices":notice,"table":time_table}
    return render(request,'Faculty/FacultyHome.html',args)

def myProfile(request):
    uid = request.session['user_id']
    path = request.session['collegeid']
    print(uid,path)
    user = database.child("users").child(uid).child("user_details").get().val()
    global user_data
    for item in user:
        user_data[item] = user[item]
    print("Faculty",user_data)
    experience = database.child("users").child(uid).child("user_details").child("experiences").get().val()
    print(experience)
    ex = []
    if experience:
        for i in experience:
            print(i)
            if i != None:
                ex.append(experience[i])
        print(ex)
    else:
        pass
        
    return render(request,'Faculty/Facultyprofile.html',{"user":user_data,'path':path, "experience" : ex})


def update(request):
    url = request.POST['imgurl']
    linkedinUrl = request.POST['Linkedinurl']
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    address1 = request.POST['add1']
    address2 = request.POST['add2']
    contry = request.POST['country']
    mobilenumber = request.POST['mobno']
    pincode = request.POST['pno']
    city = request.POST['cityss']
    user_data = {
                "linkedinurl":linkedinUrl,
                "firstname":first_name,
                "lastname":last_name,
                "address1":address1,
                "address2":address2,
                "contry":contry,
                "mobilenumber":mobilenumber,
                "pincode":pincode,
                "city":city,
                "profile_picture":url,
            }
    uid = request.session['user_id']
    print("Faculty",uid)
    database.child("users").child(uid).child("user_details").update(user_data)
    return redirect('/Faculty/profile/')

def Drive(request):
    global user_data
    path_on_cloud = request.session['collegeid']
    request.session['folder_session'] = path_on_cloud
    args = {"detail":dict(request.session['userdetails']),"path":path_on_cloud,"user":user_data}
    return render(request,'Faculty/FacultyDrive.html',args)

def uploadfile(request):
    if request.method == 'POST':
        print(request.FILES.get('file'))
        my_file = request.FILES.get('file')
        path = request.session['folder_session'] + '/' + str(my_file)  
        print(path)
        user_id_token = request.session['uid']
        storage.child(path).put(my_file, user_id_token)
    return HttpResponse('upload')

def folder_view(request, path):
    print(path)
    global user_data
    path_on_cloud_folder = path
    print(path_on_cloud_folder)
    request.session['folder_session'] = path_on_cloud_folder
    args = {"detail":dict(request.session['userdetails']),"path":path_on_cloud_folder,"new_ref":path_on_cloud_folder,"user":user_data}
    return render(request,'Faculty/FacultyDrive.html',args)

def newfolder(request):
    if request.method == 'POST':
        foldernames = request.POST['foldername1']
        path = request.POST['path'] + '/' + foldernames + '/' + 'demo'
        new_ref = request.POST['path'] + '/' + foldernames
        print(path)
        user_id_token = request.session['uid']
        storage.child(path).put("static/assets/demo.txt", user_id_token)
        print(path)
        return redirect('/Faculty/folder_view/'+new_ref)

def downloadFile(request,path):
    print(path)
    s = path.split('/')[-1]
    print(s)
    storage.child(path).download(path,s)
    return redirect('/Faculty/Drive/')
# -------------------------------------------------------------------------------------------------------------
# LEAVE
# -------------------------------------------------------------------------------------------------------------

def LeaveApplication(request):
    global user_data
    if request.method == "POST":
        f_date = request.POST['fromdate']
        date_time_from = datetime.datetime.strptime(f_date, '%Y-%m-%d')
        l_date = request.POST['tilldate']
        date_time_till = datetime.datetime.strptime(l_date, '%Y-%m-%d')
        day = date_time_till - date_time_from
        leave_report = {
            "From" : request.POST['fromdate'],
            "Till" : request.POST['tilldate'],

            "LeaveType" : request.POST['leaveType_'],
            "MobilePhoneNumber" : request.POST['Mobile'],
            "Department" : request.POST['Department'],
            "Designation" : request.POST['designation'],
            "joining" : request.POST['joiningdate'],
            "gen" : request.POST['g'], 
            "Reason" : request.POST['comments'],
            "staffname" : request.session['fname'],
            "collegeId" : request.session['collegeid'],
            "created_at" : str(datetime.datetime.now()),
            "number_of_days" : day.days,
            "leavestatus" : 0
        }
        ts = int(datetime.datetime.now().timestamp())
        print(ts)
        database.child("leaveReports").child(ts).set(leave_report)
        leaves = database.child("leaveReports").get()
        leave = []
        for i in leaves.each():
            temp = i.val()
            if temp['collegeId'] == request.session['collegeid']:
                leave.append(i.val())
        print(leave)
        
        args = {"detail":dict(request.session['userdetails']),"leaves":leave,"user":user_data}
        return render(request,"Faculty/LeaveApplication.html",args)
    
    leaves = database.child("leaveReports").get()
    leave = []
    if leaves.each() != None:
        for i in leaves.each():
            temp = i.val()
            if temp['collegeId'] == request.session['collegeid']:
                leave.append(i.val())
    print(leave)            
    args = {"detail":dict(request.session['userdetails']),"leaves":leave,"user":user_data}
    return render(request,"Faculty/LeaveApplication.html",args)

def updateExperience(request):
    checkboxcheck = request.POST['terms_and_conditions']
    uid = request.session['user_id']
    if(checkboxcheck == "signature"):
        i = random.randint(0,9)
        experiences = {
            "description" : request.POST['comments'],
            "fromdate" : request.POST['fromdate'],
            "tilldates" : "present"
        }
    if(checkboxcheck != "signature"):
        experiences = {
            "description" : request.POST['comments'],
            "fromdate" : request.POST['fromdate'],
            "tilldates" : request.POST['to']
        }
        i = random.randint(0,90)
    database.child("users").child(uid).child("user_details").child("experiences").child(i).set(experiences)
    return redirect('/Faculty/profile/')

def changepassword(request):
    email = request.session['emailid']
    firbase_auth.send_password_reset_email(email)
    return redirect('/Faculty/profile/')
