from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from argon2 import PasswordHasher
#from user.forms import UserForm

from .models import *
from main.models import TbGdCd

# Create your views here.

#개인 회원가입
def signup(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method =='POST':
        user_name = request.POST.get('user_id','')
        user_id = request.POST.get('username','')
        firstpassword = request.POST.get('password','')
        secpassword = request.POST.get('password2','')
        user_phone = request.POST.get('user_phone','')
        user_addr = request.POST.get('user_addr','')
        user_level = request.POST.get('user_level','')

        if (user_name or user_id or user_phone or firstpassword or secpassword or user_addr) == '':
            return redirect('/user/signup')
        elif firstpassword != secpassword:
            return redirect('/user/signup')
        else:
            usersave = User(username=user_id, password=PasswordHasher().hash(firstpassword), user_id=user_name , user_phone=user_phone, user_addr=user_addr,user_level=user_level)
            usersave.save()
        return redirect('main:index')

#회사 회원가입
def corpsignup(request):
    if request.method == 'GET':
        return render(request, 'user/corpsignup.html')
    elif request.method =='POST':
        user_name = request.POST.get('user_id','')
        user_id = request.POST.get('username','')
        firstpassword = request.POST.get('password','')
        secpassword = request.POST.get('password2','')
        user_phone = request.POST.get('user_phone','')
        user_addr = request.POST.get('user_addr','')
        user_level = request.POST.get('user_level','')

        if (user_name or user_id or user_phone or firstpassword or secpassword or user_addr) == '':
            return redirect('/user/signup')
        elif firstpassword != secpassword:
            return redirect('/user/signup')
        else:
            usersave = User(username=user_id, password=firstpassword, user_id=user_name , user_phone=user_phone, user_addr=user_addr, user_level=user_level)
            usersave.save()
        return redirect('main:index')

#회원가입 누르면 개인, 회사 나눠놓은것
def signselect(request):
    return render(request, 'user/signselect.html')

#로그인
def login(request):
    loginform = LoginForm()
    context = {'forms' : loginform }
    if request.method == 'GET':
        return render(request, 'user/login.html', context)
    elif request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            request.session['login_session'] = loginform.login_session
            request.session.set_expiry(0)

            return redirect('main:index')
        else:
            context['forms'] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context['error'] = value

        
        return render(request, 'user/login.html', context)

# 로그아웃
def logout(request):
    request.session.flush()
    # if request.session.get('login_session'):
    #     del request.session['login_session']
    return redirect('/')


#문의하기
def inquirys(request):
    if request.method == 'POST':
        #print(request.POST)
        inquirys_name = request.POST.get('quname')
        inquirys_email = request.POST.get('quemail')
        inquirys_text = request.POST.get('qutext')
        new_inquirys = secinquiry(inquirys_name=inquirys_name, inquirys_email=inquirys_email, inquirys_text=inquirys_text)
        new_inquirys.save()
    return render(request, 'main/index.html')


# mypage
def history_search(request):
    return render(request, 'user/history_search.html', {})

def history_sale(request):
    return render(request, 'user/history_sale.html', {})


def member_edit(request):
    return render(request, 'user/member_edit.html', {})

def sale_upload(request):
    gd_type_cd = TbGdCd.objects.only("gd_type_2").distinct()
    return render(request, 'user/sale_upload.html', {"gd_type_cd":gd_type_cd})


