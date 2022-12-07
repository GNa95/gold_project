from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from argon2 import PasswordHasher
#from user.forms import UserForm

from .models import *
from django.db import connection
from main.func import dictfetchall
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json
# Create your views here.

#개인&회사 회원가입
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

# #회사 회원가입
def corpsignup(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        sql = "select distinct ent_nm from tb_ent;"
        cursor.execute(sql)
        ent_nm = dictfetchall(cursor)
        connection.close()
        return render(request, 'user/corpsignup.html',{"ent_nms":ent_nm})
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
    return redirect('/')


# mypage
def mypage(request):
    login_session = request.session.get('login_session', '')
    userdata = User.objects.get(user_id = login_session)
    if userdata.user_level == '1':
        return render(request, 'user/history_search.html', {"login_session":login_session})
    else:
        cursor = connection.cursor()
        sql = "select id, sale_name, (select concat(group_concat(d.gd_type_2 SEPARATOR ', '),' 등') " + \
              "from (select distinct gd_type_cd from th_saled b where a.id = b.sale_id LIMIT 3) c, tb_gd_cd d where c.gd_type_cd = d.gd_type_cd) as 'sale_gds'," + \
              "(select count(*) from th_saled b where a.id = b.sale_id) as 'sale_gds_cnt'," + \
              "concat(date_format(start_date,'%Y/%m/%d'), ' ~ ', date_format(end_date,'%Y/%m/%d')) as 'sale_date'" + \
              "from th_sale a where user='" + login_session + "' order by start_date desc, end_date desc;"
        cursor.execute(sql)
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
    cursor = connection.cursor()
    if request.method == 'POST':
        sale_name = request.POST.get('sale_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        sale = ThSale(sale_name=sale_name, user=login_session, start_date=start_date, end_date=end_date)
        sale.save()
        count = request.POST.get('table_count')
        
        for i in range(1,int(count)+1):
            try:
                num = str(i)
                # gd_type_nm = request.POST.get('gd_type'+num)
                sale_gds = request.POST.get('sale_gds'+num)
                sale_price = request.POST.get('sale_price'+num)
                gd_type_sql = "select gd_type_cd from tb_gds where gd_nm = '" + sale_gds + "';"
                cursor.execute(gd_type_sql)
                gd_type_cd = cursor.fetchall()[0][0]
                sale_detail = ThSaleDetail(sale=sale, gd_type_cd=gd_type_cd, sale_gds=sale_gds , sale_price=sale_price)
                sale_detail.save()
            except:
                pass
        return redirect('user:mypage')
    sql = "select distinct(gd_nm) from tb_gds;"
    cursor.execute(sql)
    gd_nms = dictfetchall(cursor)
    connection.close()
    return render(request, 'user/sale_upload.html', {"gd_nms":gd_nms, "login_session":login_session})

def sale_edit(request, sale_id):
    login_session = request.session.get('login_session', '')
    sale = get_object_or_404(ThSale, pk=sale_id)
    saleSql = "select gd_type_2, sale_gds, sale_price from th_saled a, tb_gd_cd b where a.gd_type_cd = b.gd_type_cd and sale_id = " + str(sale_id) +";"
    cursor = connection.cursor()
    cursor.execute(saleSql)
    saled = dictfetchall(cursor)
    connection.close()
    return render(request, 'user/sale_edit.html', {"sale":sale,"saled":saled,"login_session":login_session})

@csrf_exempt
def ent_search(request):
    jsonObject = json.loads(request.body)
    ent_nm =   jsonObject.get('ent_nm')
    entsql = "select * from tb_ent where ent_nm ='" + ent_nm + "';"
    usersql = "select * from tb_user where username='" + ent_nm + "';"
    cursor = connection.cursor()
    cursor.execute(entsql)
    ent_info = dictfetchall(cursor)
    cursor.execute(usersql)
    user_info = dictfetchall(cursor)
    connection.close()
    if ent_info:
        if user_info:
            return JsonResponse({"alert":"이 업체는 이미 존재합니다."})
        return JsonResponse(ent_info[0])
    return JsonResponse({"alert":"찾으시는 업체가 없습니다."})
    

@csrf_exempt
def idCheck(request):
    jsonObject = json.loads(request.body)
    user_id = jsonObject.get('user_id')
    usersql = "select * from tb_user where user_id ='" + user_id + "';"
    cursor = connection.cursor()
    cursor.execute(usersql)
    user_info = dictfetchall(cursor)
    connection.close()
    if user_info:
        return JsonResponse({"alert":"아이디가 이미 존재합니다."})
    return JsonResponse({})