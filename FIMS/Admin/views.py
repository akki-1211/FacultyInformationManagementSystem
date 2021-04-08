from django.shortcuts import render
import pyrebase
from django.contrib import messages,auth
from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse
import datetime
from numpy import random
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .utils import generate_token
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
from firebase_admin import auth


# Create your views here.
user_data = {}
def AdminHome(request):
    uid = request.session['user_id']
    user = database.child("users").child(uid).child("user_details").get().val()
    collegeid = request.session['collegeid']
    global user_data

    time_table = {}
    table = database.child("Timetable").get().val()
    print(table)
    if table:
        for t in table:
            time_table[t] = table[t]

    for item in user:
        user_data[item] = user[item]
    notices = database.child("Notice").get()
    notice = dict()
    if(notices != None):
        for i in notices.each():
            notice[i.key()] = i.val()
   
    args = {"detail":dict(request.session['userdetails']),"user":user_data,"notices":notice,"table":time_table}
    return render(request,'Admin/AdminHome.html',args)

def myProfile(request):
    uid = request.session['user_id']
    path = request.session['collegeid']
    print(uid,path)
    user = database.child("users").child(uid).child("user_details").get().val()
    global user_data
    for item in user:
        user_data[item] = user[item]
    print("Admin",user_data)
    # return redirect('/Faculty/Drive/')
    return render(request,'Admin/Adminprofile.html',{"user":user_data,'path':path})

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
                "country":contry,
                "mobilenumber":mobilenumber,
                "pincode":pincode,
                "city":city,
                "profile_picture":url,
            }
    uid = request.session['user_id']
    print("Admin",uid)
    database.child("users").child(uid).child("user_details").update(user_data)
    return redirect('/Admin/profile/')

def ViewUsers(request):
    global user_data
    allfaculty = database.child("users").get()
    faculty = dict()
    if(allfaculty != None):
        for i in allfaculty.each():
            faculty[i.key()] = i.val()   
    args = {"detail":dict(request.session['userdetails']),"facultydetails":faculty,"user":user_data}
    return render(request,'Admin/ViewUser.html',args)

def AddUser(request):
    global user_data
    if request.method == 'POST':
        job_post = request.POST['selectuserrole']
        department_name = request.POST['selectdepartment']
        linkedinUrl = request.POST['Linkedinurl']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        address1 = request.POST['add1']
        address2 = request.POST['add2']
        country = request.POST['selectcountry']
        mobilenumber = request.POST['mobno']
        email_id = request.POST['email']
        pincode = request.POST['pno']
        city = request.POST['cityss']
        user_password = request.POST['pass']
        confirm_user_password = request.POST['rpass']

        CollegeId = UserIDGenrator(job_post)

        if(user_password == confirm_user_password):
            user = firbase_auth.create_user_with_email_and_password(email_id,user_password)
            print(user)
            user_id = user['localId']
            print(user_id)
            user_details = {
                "job":job_post,
                "department":department_name,
                "linkedinurl":linkedinUrl,
                "collegeid":CollegeId,
                "firstname":first_name,
                "lastname":last_name,
                "address1":address1,
                "address2":address2,
                "country":country,
                "mobilenumber":mobilenumber,
                "pincode":pincode,
                "city":city,
                "profile_picture":"https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHByb2ZpbGV8ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=60",
                "Active":'False',
                "leavedays":730,
            }
            
            # current_site=get_current_site(request)
            # email_subject = 'Activate Your Account' 
            # message = render_to_string('layout/activate.html',
            # {
            #     'user':user,
            #     'domain':current_site,
            #     'uid':urlsafe_base64_encode(force_bytes(user_id)),
            # }
            # )               
            # email = EmailMessage(
            #     email_subject,
            #     message,
            #     'noreply@semycolon.com',
            #     [email_id],
            #     )
            # email.send(fail_silently=False)  

                #database.push(user_data)
            firbase_auth.send_email_verification(user['idToken'])    
            database.child("users").child(user_id).child("user_details").set(user_details)
            messages.error(request,'Successfully Recruited A Faculty')
            return redirect('/Admin/AddUsers/')
        else:
            messages.error(request,'An error occured')
            return redirect('/Admin/AddUsers/')
    args = {"detail":dict(request.session['userdetails']),"user":user_data}
    return render(request,'Admin/AddUser.html',args)

def addTimeTable(request):
    global user_data
    collegeid = request.session['collegeid']
    time_table = {}
    table = database.child("Timetable").get().val()
    if table:
        for t in table:
            time_table[t] = table[t]
        print(time_table)
    u = database.child("users").get().val()
    staff = {}
    for user in u:
        staff[u[user]["user_details"]["collegeid"]] = u[user]["user_details"]["firstname"] + " " + u[user]["user_details"]["lastname"]
    if request.method == "POST":
        day = request.POST['day']
        lec1 = request.POST['lec1']
        lec2 = request.POST['lec2']
        lec3 = request.POST['lec3']
        lec4 = request.POST['lec4']
        lab = request.POST['lab']

        lec1staff = request.POST['lec1staff']
        lec2staff = request.POST['lec2staff']
        lec3staff = request.POST['lec3staff']
        lec4staff = request.POST['lec4staff']
        labstaff = request.POST['labstaff']

        lec1fromdate = request.POST['lec1fromdate']
        lec2fromdate = request.POST['lec2fromdate']
        lec3fromdate = request.POST['lec2fromdate']
        lec4fromdate = request.POST['lec3fromdate']
        labfromdate = request.POST['labfromdate']

        lec1tilldate = request.POST['lec1tilldate']
        lec2tilldate = request.POST['lec2tilldate']
        lec3tilldate = request.POST['lec3tilldate']
        lec4tilldate = request.POST['lec4tilldate']
        labtilldate = request.POST['labtilldate']

        Add_day = {
            "lec1":lec1,
            "lec1staff":lec1staff,
            "lec1fromtime":lec1fromdate,
            "lec1tilltime":lec1tilldate,
            "lec2":lec2,
            "lec2staff":lec2staff,
            "lec2fromtime":lec2fromdate,
            "lec2tilltime":lec2tilldate,
            "lec3":lec3,
            "lec3staff":lec3staff,
            "lec3fromtime":lec3fromdate,
            "lec3tilltime":lec3tilldate,
            "lec4":lec4,
            "lec4staff":lec4staff,
            "lec4fromtime":lec4fromdate,
            "lec4tilltime":lec4tilldate,
            "lab":lab,
            "labstaff":lec1staff,
            "labfromtime":lec1fromdate,
            "labtilltime":lec1tilldate
        }
        database.child("Timetable").child(day).set(Add_day)        
        time_table = {}
        table = database.child("Timetable").get().val()
        for t in table:
            time_table[t] = table[t]
        return render(request,'Admin/CreateTimeTable.html',{"staff": staff,"table":time_table,"user":user_data})
    else:
        return render(request,'Admin/CreateTimeTable.html',{"staff": staff,"table":time_table,"user":user_data})


def AllLeaveRequest(request):
    global user_data
    leave = database.child("leaveReports").get()
    print(leave)
    req = 0
    leaves = dict()
    if leave.each() !=  None:
        for i in leave.each():
            leaves[i.key()] = i.val()
            temp = i.val()
            if temp['leavestatus'] == 0:
                req += 1
    args = {"detail":dict(request.session['userdetails']),"leaves":leaves,"req":req,"user":user_data}
    return render(request,'Admin/AllLeaveRequested.html',args)  

def PendingRequest(request):
    global user_data
    leave = database.child("leaveReports").get()
    print(leave)
    req = 0
    leaves = dict()
    if leave.each() !=  None:
        for i in leave.each():
            temp = i.val()
            if temp['leavestatus'] == 0:
                leaves[i.key()] = i.val()
                req += 1
    args = {"detail":dict(request.session['userdetails']),"leaves":leaves,"req":req,"user":user_data}
    return render(request,'Admin/AllLeaveRequested.html',args)     


def ApprovedRequest(request):
    global user_data
    leave = database.child("leaveReports").get()
    print(leave)
    req = 0
    leaves = dict()
    if leave.each() !=  None:
        for i in leave.each():
            temp = i.val()
            if temp['leavestatus'] == 1:
                leaves[i.key()] = i.val()
            if temp['leavestatus'] == 0:
                req += 1       
    args = {"detail":dict(request.session['userdetails']),"leaves":leaves,"req":req,"user":user_data}
    return render(request,'Admin/AllLeaveRequested.html',args)   


def CancelRequest(request):
    global user_data
    leave = database.child("leaveReports").get()
    print(leave)
    req = 0
    leaves = dict()
    if leave.each() !=  None:
        for i in leave.each():
            temp = i.val()
            if temp['leavestatus'] == 2:
                leaves[i.key()] = i.val()
            if temp['leavestatus'] == 0:
                req += 1    
    args = {"detail":dict(request.session['userdetails']),"leaves":leaves,"req":req,"user":user_data}
    return render(request,'Admin/AllLeaveRequested.html',args)   


def approve_leave(request,id):
    database.child("leaveReports").child(id).update({'leavestatus':1})
    return redirect("/Admin/AllLeaveRequest/")

def disapprove_leave(request,id):
    database.child("leaveReports").child(id).update({'leavestatus':2})
    return redirect("/Admin/AllLeaveRequest/")

def UserIDGenrator(job):
    x = datetime.datetime.now()
    Year = x.strftime("%Y")
    if(job == "Admin"):
        job_value = "ADM" 
    else:
        job_value = "FAC" 
    rand = str(random.randint(999999))  
    UserId = Year+job_value+rand
    return UserId     

def Drive(request):
    global user_data
    path_on_cloud = request.session['collegeid']
    request.session['folder_session'] = path_on_cloud
    args = {"detail":dict(request.session['userdetails']),"path":path_on_cloud,"user":user_data}
    return render(request,'Admin/AdminDrive.html',args)

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
    global user_data
    print(path)
    path_on_cloud_folder = path
    print(path_on_cloud_folder)
    request.session['folder_session'] = path_on_cloud_folder
    args = {"detail":dict(request.session['userdetails']),"path":path_on_cloud_folder,"new_ref":path_on_cloud_folder,"user":user_data}
    return render(request,'Admin/AdminDrive.html',args)

def newfolder(request):
    if request.method == 'POST':
        foldernames = request.POST['foldername1']
        path = request.POST['path'] + '/' + foldernames + '/' + 'demo'
        new_ref = request.POST['path'] + '/' + foldernames
        print(path)
        user_id_token = request.session['uid']
        storage.child(path).put("static/assets/demo.txt", user_id_token)
        print(path)
        return redirect('/Admin/folder_view/'+new_ref)

def AddNotice(request):
    title = request.POST['Title']
    description = request.POST['ShortDescription']
    
    ts = int(datetime.datetime.now().timestamp())
    print(ts)
    noticedetails = {
        "title" : title,
        "description" : description,
        "id" : ts
    }
    ts = int(datetime.datetime.now().timestamp())
    print(ts)
    database.child("Notice").child(ts).set(noticedetails)
    return redirect('/Admin/')

def removeNotice(request,id):
    database.child("Notice").child(id).remove()
    return redirect("/Admin/")

def removeUser(request,id):
    auth.delete_user(id)
    database.child("users").child(id).child("user_details").set(user_data)
    return redirect("/Admin/ViewUsers/")


