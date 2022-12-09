from django.shortcuts import render
from django.db import connection
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from .func import crawl
from .models import *
from django.utils.dateformat import DateFormat
from datetime import datetime
from .func import crawl, dictfetchall
# Create your views here.

def index(request):
  login_session = request.session.get('login_session', '')
  return render(request, 'main/index.html', {"login_session" : login_session})

@csrf_exempt
def second(request):
  #stt변수에 POST방식으로 'stt' 값을 전달 받는다. GET과 POST를 알아야한다.
  login_session = request.session.get('login_session', '')
  stt = request.POST.get('stt','')
  # print("111", stt)  #이 프린트는 딜레이해결 완료 할때까지 잠시 대기입니다.
  stt_edit = stt.replace(' ',"%")
  cursor = connection.cursor()
  recipeSql = "select recipe_nm from tb_recipe where recipe_nm like '"+ stt_edit + "' limit 1;"
  cursor.execute(recipeSql)
  recipeRst = cursor.fetchall()
  
  if recipeRst:
    recipe_nm = recipeRst[0][0]
    strSql = "select tb_irdent.gd_type_cd, irdnt_nm, gd_nm, gd_num, gd_ent_nm "\
            + "from tb_recipe join tb_irdent on tb_recipe.recipe_num = tb_irdent.recipe_num join tb_gds on tb_irdent.gd_type_cd = tb_gds.gd_type_cd "\
            + "where recipe_nm like '"+ recipe_nm + "' order by rand();"

    cursor.execute(strSql)
    result = cursor.fetchall()
    connection.close()
    df = pd.DataFrame(result,columns=['gd_type_cd', 'irdnt_nm', 'gd_nm', 'gd_num', 'gd_ent_nm'])
    irdent = df.drop_duplicates(['gd_type_cd']).sort_values('gd_type_cd')
    irdent_dict = irdent.T.to_dict()
  else:
    irdent_dict = ""
    recipe_nm = stt

  return render(request, 'main/second.html',{"irdent_dict":irdent_dict, "login_session":login_session, "recipe_nm":recipe_nm})

@csrf_exempt
def third(request):
  login_session = request.session.get('login_session', '')
  lon = request.POST.get("lon")
  lat = request.POST.get("lat")
  cursor = connection.cursor()
  sqlMap = "select ent_num, ent_nm, map_y, map_x,ent_phone,ent_addr, dense_rank() over (order by ST_DISTANCE_SPHERE(POINT("+lon+", "+lat+"), POINT(map_y, map_x))) as ranking from tb_ent limit 3;"

  cursor.execute(sqlMap)
  result_map = dictfetchall(cursor)
  connection.close()

  ent = [i["ent_num"] for i in result_map ]
  ent_nm = [i["ent_nm"] for i in result_map]
  
  irdent = request.POST.get("irdent")
  checked = request.POST.get('checked')
  irdent = eval(irdent)
  checked = checked.split()
  
  df = pd.DataFrame(irdent).T
  df = df[df["gd_num"].isin(list(map(int,checked)))]

  good = df['gd_num'].tolist()

  df['mart1'] = None
  df['mart2'] = None
  df['mart3'] = None
  df = df.set_index('gd_num') 

  print("api 동작")
  cost = crawl(good, ent)
  print("api 동작완료")
  
  for i,j in cost.items():
    for key, value in j.items():
      df.loc[key,[i]] = value
      
  # 소숫점 format 
  df = df.fillna(0)
  df[['mart1', 'mart2', 'mart3']] = df[['mart1', 'mart2', 'mart3']].astype(int)
  
  for i, j in enumerate(result_map):
    j['mart'] = format(int(df['mart'+str(i+1)].sum()), ',')
  
  df = df.replace(0,"미제공")
  irdent_all = df.T.to_dict()

  dentJson = json.dumps(result_map, ensure_ascii=False)
  
  result_map.reverse()
  
  # 검색이력
  recipe_name =  request.POST.get('recipe')
  today = DateFormat(datetime.now()).format('Ymd')
  
  TBsearch = ThSearch1(user_id=login_session, recipe_nm=recipe_name, ht_date=today)
  TBsearch.save()
  search_id = TBsearch.id
  for row in df.itertuples():
    TBsearch = ThSearch2(search_id=search_id, irdnt_nm=row[2], gd_nm=row[3])
    TBsearch.save()
  
  return render(request, 'main/third.html',{"ent_list":dentJson, 'map_list':result_map, 'ent_nm':ent_nm, "login_session":login_session, 'irdent_all':irdent_all})
