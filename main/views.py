from django.shortcuts import render
from django.db import connection
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from .func import crawl
# Create your views here.

def index(request):
  login_session = request.session.get('login_session', '')
  return render(request, 'main/index.html', {"login_session" : login_session})

@csrf_exempt
def second(request):
  #stt변수에 POST방식으로 'stt' 값을 전달 받는다. GET과 POST를 알아야한다.
  stt = request.POST.get('stt','')
  cursor = connection.cursor()
  strSql = "select * from tb_recipe r, tb_irdent i where r.recipe_num = i.recipe_num and r.recipe_nm like '"+ stt + "';"
  cursor.execute(strSql)
  result = cursor.fetchall()
  connection.close()
  #이 아래 프린트는 딜레이해결 완료 할떄까지 잠시 대기입니다.
  print("111", stt)

  irdent = []
  for data in result:
    row = {
      'idn': data[7]
    }
    irdent.append(row)

  return render(request, 'main/second.html',{"irdent":irdent})

def third(request):
  lon = "126.982732"
  lat = "37.488236"
  test = "냉면"
  cursor = connection.cursor()
  sqlAll = "select IRDNT_NM, GD_NUM, tb_irdent.GD_TYPE_CD, GD_NM, GD_ENT_NM "\
          + "from tb_recipe join tb_irdent on tb_recipe.RECIPE_NUM = tb_irdent.RECIPE_NUM join tb_gds on tb_irdent.GD_TYPE_CD = tb_gds.GD_TYPE_CD "\
          + "where RECIPE_NM like '"+ test + "' order by rand();"
  sqlMap = "select ENT_NUM, ENT_NM, MAP_Y, MAP_X,ENT_PHONE,ENT_ADDR, dense_rank() over (order by ST_DISTANCE_SPHERE(POINT("+lon+", "+lat+"), POINT(MAP_Y, MAP_X))) as ranking from tb_ent limit 3;"

  cursor.execute(sqlAll)
  result_all = cursor.fetchall()
  cursor.execute(sqlMap)
  result_map = cursor.fetchall()
  connection.close()

  map = []
  for data in result_map:
    row = {
      'ent_nm': data[0],
      'map_y': data[1],
      'map_x': data[2],
      'ent_phone': data[3],
      'ent_addr': data[4]
    }
    map.append(row)


  ent = [i[0] for i in result_map ]
  
  df = pd.DataFrame(result_all,columns=['irdnt_nm','gd_num', 'gd_type_cd', 'gd_nm','gd_ent_nm'])
  irdent = df.drop_duplicates(['gd_type_cd']).sort_values('gd_type_cd')
  
  good_col = irdent['gd_num'].values
  good = good_col.tolist()
  
  print("api 동작")
  cost = crawl(good, ent)
  print("api 동작완료")
  
  df2 = pd.DataFrame(cost).T
  df2 = df2.reset_index()
  df2 = df2.rename(columns={'index':'gd_num'})

  merdf = pd.merge(irdent, df2, how='outer').fillna(0)
  sum = merdf.sum().to_dict()
  irdent_all = merdf.T.to_dict()

  dentJson = json.dumps(map, ensure_ascii=False)

  return render(request, 'main/third.html',{"irdent_all":irdent_all, "ent_list":dentJson, 'ent':ent, 'sum':sum})