from django.shortcuts import render
from django.db import connection
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
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
  print("111", stt)  #이 프린트는 딜레이해결 완료 할때까지 잠시 대기입니다.
  stt_edit = stt.replace(' ',"%")
  cursor = connection.cursor()
  recipeSql = "select recipe_nm from tb_recipe where recipe_nm like '"+ stt_edit + "' limit 1;"
  cursor.execute(recipeSql)
  recipeRst = cursor.fetchall()
  
  if recipeRst:
    recipe_nm = recipeRst[0][0]
    strSql = "select tb_irdent.GD_TYPE_CD, IRDNT_NM, GD_NM, GD_NUM, GD_ENT_NM "\
            + "from tb_recipe join tb_irdent on tb_recipe.RECIPE_NUM = tb_irdent.RECIPE_NUM join tb_gds on tb_irdent.GD_TYPE_CD = tb_gds.GD_TYPE_CD "\
            + "where RECIPE_NM like '"+ recipe_nm + "' order by rand();"

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
  lon = request.POST.get("lon")
  lat = request.POST.get("lat")
  cursor = connection.cursor()
  sqlMap = "select ent_num, ent_nm, map_y, map_x,ent_phone,ent_addr, dense_rank() over (order by ST_DISTANCE_SPHERE(POINT("+lon+", "+lat+"), POINT(MAP_Y, MAP_X))) as ranking from tb_ent limit 3;"

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
  
  good_col = df['gd_num']
  good = good_col.tolist()
  
  print("api 동작")
  cost = crawl(good, ent)
  print("api 동작완료")
  
  df2 = pd.DataFrame(cost).T
  df2 = df2.reset_index()
  df2 = df2.rename(columns={'index':'gd_num'})

  merdf = pd.merge(df, df2, how='outer').fillna(0)
  merdf[['mart1', 'mart2', 'mart3']] = merdf[['mart1', 'mart2', 'mart3']].astype(int)
  for i, j in enumerate(result_map):
    j['mart'] = format(int(merdf['mart'+str(i+1)].sum()), ',')
  
  merdf = merdf.replace(0,"미제공")
  irdent_all = merdf.T.to_dict()

  dentJson = json.dumps(result_map, ensure_ascii=False)
  
  result_map.reverse()

  return render(request, 'main/third.html',{"ent_list":dentJson, 'irdent_all':irdent_all, 'map_list':result_map, 'ent_nm':ent_nm}) 