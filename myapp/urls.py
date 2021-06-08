from collections import namedtuple
from . import views
from django.urls import path

urlpatterns = [
    path('',views.register,name="register"),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name="logout"),
    path('upload/',views.image_view,name="image_view"),
    path('uploaded/', views.image_upload_view,name="image_upload_view"),
    path('profile/',views.profile,name='profile'),
    path('profiles/',views.profiles,name='profiles'),
    path('myprofile/',views.myprofile,name='myprofile')
]

