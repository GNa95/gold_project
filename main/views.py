from django.shortcuts import render
from main.models import TbRecipe,TbIrdent
from django.db import connection
from django.db.models import Q
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
  sqlIrdent = "select irdnt_nm,r.recipe_num from tb_recipe r, tb_irdent i where r.recipe_num = i.recipe_num and r.recipe_nm like '"+ test + "';"
  sqlSum = "select sum(r.recipe_num) from tb_recipe r, tb_irdent i where r.recipe_num = i.recipe_num and r.recipe_nm like '"+ test + "';"
  sqlDan = "select tb_gds.GD_NM, tb_gds.GD_UNIT, tb_gds.GD_UNIT_CD, tb_irdent.IRDNT_NM, tb_recipe.RECIPE_NUM from tb_recipe join tb_irdent on tb_recipe.RECIPE_NUM = tb_irdent.RECIPE_NUM join tb_gds on tb_irdent.GD_TYPE_CD = tb_gds.GD_TYPE_CD where RECIPE_NM like '"+ test + "';"

  cursor.execute(sqlIrdent)
  result_irdent = cursor.fetchall()
  cursor.execute(sqlSum)
  result_sum = cursor.fetchall()
  cursor.execute(sqlDan)
  result_dan = cursor.fetchall()
  connection.close()

  irdent = []
  for data in result_irdent:
    row = {
      'idn': data[0],
      'num': data[1]
    }
    irdent.append(row)

  sum = []
  for data in result_sum:
    row = {
      'add': data[0]
    }
    sum.append(row)

  dan = []
  for data in result_dan:
    row = {
      'dan1': data[1],
      'dan2': data[2],
      'idn': data[0],
      'num': data[4]

    }
    dan.append(row)

  return render(request, 'main/third.html',{"irdent":irdent,"sum":sum,"dan":dan})


