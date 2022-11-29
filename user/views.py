from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, SaleForm
from django.contrib.auth import login, authenticate
from argon2 import PasswordHasher
#from user.forms import UserForm

from .models import *
from main.models import TbGdCd
from django.db import connection

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
            usersave = User(username=user_id, password=PasswordHasher().hash(firstpassword), user_id=user_name , user_phone=user_phone, user_addr=user_addr, user_level=user_level)
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
        print("들어감감?")
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
                    print("들어감?")

        
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
def mypage(request):
    login_session = request.session.get('login_session', '')
    userdata = User.objects.get(user_id = login_session)
    if userdata.user_level == '1':
        return render(request, 'user/history_search.html', {"login_session":login_session})
    else:
        cursor = connection.cursor()
        sql = "select id, sale_name," + \
              "(select concat(group_concat(gd_type_nm SEPARATOR ', '),' 등') from (select gd_type_nm from th_saled b where a.id = b.sale_id LIMIT 3) c) as 'sale_gds'," + \
              "(select count(*) from th_saled b where a.id = b.sale_id) as 'sale_gds_cnt'," + \
              "concat(date_format(start_date,'%Y/%m/%d'), ' ~ ', date_format(end_date,'%Y/%m/%d')) as 'sale_date'" + \
              "from th_sale a where user='" + login_session + "' order by end_date desc, start_date desc;"
        cursor.execute(sql)
        # result = cursor.fetchall()
        result = dictfetchall(cursor)
        cursor.close()
        return render(request, 'user/history_sale.html', {"sale_data":result, "login_session":login_session})

def member_edit(request):
    login_session = request.session.get('login_session', '')
    userdata = User.objects.get(user_id = login_session)
    if request.method == 'POST':
        phone = request.POST.get('phone')
        addr = request.POST.get('addr')
        if phone:
            userdata.user_phone = phone 
        if addr:
            userdata.user_addr = addr
        userdata.save()
        return render(request, 'user/member_save.html', {"login_session":login_session})
    
    return render(request, 'user/member_edit.html', {"userdata":userdata, "login_session":login_session})

def sale_upload(request):
    login_session = request.session.get('login_session', '')
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = login_session
            sale.save()
        count = request.POST.get('table_count')
        for i in range(1,int(count)+1):
            try:
                num = str(i)
                gd_type_nm = request.POST.get('gd_type'+num)
                sale_gds = request.POST.get('sale_gds'+num)
                sale_price = request.POST.get('sale_price'+num)
                sale_detail = ThSaleDetail(sale=sale, gd_type_nm=gd_type_nm, sale_gds=sale_gds , sale_price=sale_price)
                sale_detail.save()
            except:
                pass
        return redirect('user:mypage')
    gd_type_cd = TbGdCd.objects.only("gd_type_2").distinct()
    return render(request, 'user/sale_upload.html', {"gd_type_cd":gd_type_cd, "login_session":login_session})

def sale_edit(request, sale_id):
    login_session = request.session.get('login_session', '')
    sale = get_object_or_404(ThSale, pk=sale_id)
    saled = ThSaleDetail.objects.filter(sale=sale)
    return render(request, 'user/sale_edit.html', {"sale":sale,"saled":saled,"login_session":login_session})







def dictfetchall(cursor):
  columns = [col[0] for col in cursor.description]
  return [
    dict(zip(columns, row))
    for row in cursor.fetchall()
  ]