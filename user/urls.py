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


    # mypage
    path('history_search/',views.history_search, name='history_search'),
    path('history_sale/',views.history_sale, name='history_sale'),
    path('edit/',views.member_edit, name='member_edit'),
    path('upload/',views.sale_upload, name='sale_upload'),

]