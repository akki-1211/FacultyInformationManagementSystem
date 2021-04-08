"""FacultyInformationSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Admin import views

urlpatterns = [
    path('', views.AdminHome, name='AdminHome'),
    path('profile/', views.myProfile, name='myProfile'),
    path('updateProfile/', views.update, name='update'),
    path('addTable/', views.addTimeTable, name='addTimeTable'),

    #User management
    path('ViewUsers/', views.ViewUsers, name='ViewUsers'),
    path('AddUsers/', views.AddUser, name='AddUsers'),
    
    path('removeUser/<str:id>', views.removeUser, name='removeUser'),
    
    path('AddNotice/', views.AddNotice, name='AddNotice'),
    
    path('removeNotice/<str:id>', views.removeNotice, name='removeNotice'),

    #Leave management
    path('AllLeaveRequest/', views.AllLeaveRequest, name='AllLeaveRequest'),
    
    path('PendingRequest/', views.PendingRequest, name='PendingRequest'),
    
    path('ApprovedRequest/', views.ApprovedRequest, name='ApprovedRequest'),
    
    path('CancelRequest/', views.CancelRequest, name='CancelRequest'),

    path('approve_leave/<str:id>', views.approve_leave, name='approve_leave'),
    path('disapprove_leave/<str:id>', views.disapprove_leave, name='disapprove_leave'),

    #MY Drive
    path('Drive/', views.Drive, name='Drive'),
    path('file_upload/', views.uploadfile, name='uploadfile'),
    path('folder_view/<path:path>/', views.folder_view, name='folderview'),
    path('new_folder/', views.newfolder, name='newfolder'),
    
]
