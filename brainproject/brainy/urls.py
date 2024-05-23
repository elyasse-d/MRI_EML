from django.contrib import admin
from django.urls import path
from brainy import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm


urlpatterns = [
   path('',views.Home,name='home' ),  
   path("login/", views.CustomLoginView.as_view(), name="login"),
   path('signup/', views.signup, name='signup'),
   path('profile/', views.profil, name='profile'),
   path('edit_profile/', views.edit_profile, name='edit_profile'),
   path('logout/', views.custom_logout_view, name='logout'),
   path("majority/", views.Majority.as_view(), name="majority"),
   path("HistoryScan/", views.HistoryScan.as_view(), name="HistoryScan"),
   path("init/", views.achivmenet, name="home"),
]