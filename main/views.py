from django.shortcuts import render
from main.models import TbRecipe,TbIrdent,TbGds,TbEnt
from django.db import connection
from pandas import DataFrame
import pandas as pd
import json
# Create your views here.

def index(request):
  login_session = request.session.get('login_session', '')
  return render(request, 'main/index.html', {"login_session" : login_session})
  
def second(request):
  test = request.GET.get('test', 'none')
  cursor = connection.cursor()
  strSql = "select * from tb_recipe r, tb_irdent i where r.recipe_num = i.recipe_num and r.recipe_nm like '"+ test + "';"
  cursor.execute(strSql)
  result = cursor.fetchall()
  connection.close()

  irdent = []
  for data in result:
    row = {
      'idn': data[7]
    }
    irdent.append(row)

  return render(request, 'main/second.html',{"irdent":irdent})

def third(request):
  test = "냉면"
  cursor = connection.cursor()
  sqlSum = "select sum(r.recipe_num) from tb_recipe r, tb_irdent i where r.recipe_num = i.recipe_num and r.recipe_nm like '"+ test + "';"
  sqlAll = "select tb_recipe.RECIPE_NUM, IRDNT_NM, tb_gds.gd_type_cd, GD_NM, GD_ENT_NM "\
          + "from tb_recipe join tb_irdent on tb_recipe.RECIPE_NUM = tb_irdent.RECIPE_NUM join tb_gds on tb_irdent.GD_TYPE_CD = tb_gds.GD_TYPE_CD "\
          + "where RECIPE_NM like '"+ test + "' order by rand();"
  sqlMap = "select ENT_NM, concat(MAP_X,',', MAP_Y) from (SELECT ENT_NM,ENT_ADDR,MAP_X,MAP_Y FROM golddb.tb_ent) A;"

  cursor.execute(sqlSum)
  result_sum = cursor.fetchall()
  cursor.execute(sqlAll)
  result_all = cursor.fetchall()
  cursor.execute(sqlMap)
  result_map = cursor.fetchall()
  connection.close()

  # print(result_map)

  sum = []
  for data in result_sum:
    row = {
      'add': data[0]
    }
    sum.append(row)

  map = []
  for data in result_map:
    row = {
      'title': data[0],
      'latlng': data[1]
    }
    map.append(row)
  # print(map)

  df = pd.DataFrame(result_all,columns=['num','name','type','goods','jejosa'])
  irdent = df.drop_duplicates(['type']).sort_values('type')
  irdent_all = irdent.T.to_dict()

  # mf = pd.DataFrame(result_map,columns=['title','latlng'])
  # map_addr = mf.T.to_dict()

  return render(request, 'main/third.html',{"irdent_all":irdent_all,"sum":sum,"map":map})