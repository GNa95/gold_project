from django.shortcuts import render
from main.models import TbRecipe,TbIrdent,TbGds
from django.db import connection
import random
from pandas import DataFrame
import pandas as pd
# Create your views here.

def index(request):
  return render(request, 'main/index.html', {})

def second(request):
  test = "냉면"
  cursor = connection.cursor()
  strSql = "select * from tb_recipe r, tb_irdent i where r.recipe_num = i.recipe_num and r.recipe_nm like '"+ test + "';"
  cursor.execute(strSql)
  result = cursor.fetchall()
  
  # print(result)
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
  sqlAll = "select * from tb_recipe join tb_irdent on tb_recipe.RECIPE_NUM = tb_irdent.RECIPE_NUM join tb_gds on tb_irdent.GD_TYPE_CD = tb_gds.GD_TYPE_CD where RECIPE_NM like '"+ test + "' order by rand();"

  cursor.execute(sqlSum)
  result_sum = cursor.fetchall()
  cursor.execute(sqlAll)
  result_all = cursor.fetchall()
  connection.close()

  sum = []
  for data in result_sum:
    row = {
      'add': data[0]
    }
    sum.append(row)

  all = []
  for data in result_all:
    row = {
      'num': data[0],
      'name': data[7],
      'type': data[9],
      'menu': data[12],
      'jejosa': data[16]
    }
    all.append(row)

  df = pd.DataFrame(all,columns=['num','name','type','menu','jejosa'])
  irdent = df.drop_duplicates(['type']).sort_values('type')
  irdent_all = irdent.values.tolist()

  alls = []
  for data in irdent_all:
    row = {
      'num': data[0],
      'name': data[1],
      'menu': data[3],
      'jejosa': data[4]
    }
    alls.append(row)

  return render(request, 'main/third.html',{"alls":alls,"sum":sum})


