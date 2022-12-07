from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import inquirys

app_name = 'user'

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('corpsignup/',views.corpsignup, name='corpsignup'),
    path('signselect/',views.signselect, name='signselect'),

    path('', inquirys, name='inquirys'), #문의하기 데이터를 처리할 URL


    path('idCheck/',views.idCheck, name="idCheck"),
    path('ent_search/',views.ent_search, name="ent_search"),

    # mypage
    path('mypage/',views.mypage, name='mypage'),
    path('edit/',views.member_edit, name='member_edit'),
    path('upload/',views.sale_upload, name='sale_upload'),
    path('sale_edit/<int:sale_id>/',views.sale_edit, name='sale_edit'),

]