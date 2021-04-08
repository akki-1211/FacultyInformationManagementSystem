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
from Faculty import views

urlpatterns = [
    path('', views.FacultyHome, name='FacultyHome'),
    path('Drive/', views.Drive, name='Drive'),
    path('profile/', views.myProfile, name='myProfile'),
    path('updateProfile/', views.update, name='update'),
    path('updateExperience/', views.updateExperience, name='updateExperience'),
    path('changepassword/', views.changepassword, name='changepassword'),
    #file operation
    path('file_upload/', views.uploadfile, name='uploadfile'),
    path('folder_view/<path:path>/', views.folder_view, name='folderview'),
    path('new_folder/', views.newfolder, name='newfolder'),
    # path('delete_file/<str:filename>', views.deletefile, name='deletefile'),
    path('LeaveApplication/', views.LeaveApplication, name='LeaveApplication'),
    path('downloadFile/<path:path>/', views.downloadFile, name='downloadFile'),
]
