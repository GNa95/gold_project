from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import inquirys

app_name = 'user'

urlpatterns = [
    # path('login/',auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('signup/',views.signup, name='signup'),


    path('login/', views.login, name='login'),
    path('signup/',views.signup, name='signup'),

    path('corpsignup/',views.corpsignup, name='corpsignup'),
    path('signselect/',views.signselect, name='signselect'),

    path('', inquirys, name='inquirys') #문의하기 데이터를 처리할 URL


]