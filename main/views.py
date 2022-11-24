from django.shortcuts import render
from main.models import TbRecipe,TbIrdent
from django.db import connection
from django.db.models import Q
# Create your views here.

def index(request):
  return render(request, 'main/index.html', {})

def test(request):
  test = "호박죽"
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

  return render(request, 'main/test.html', {"irdent":irdent})

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

  cursor.execute(sqlIrdent)
  result_irdent = cursor.fetchall()
  cursor.execute(sqlSum)
  result_sum = cursor.fetchall()
  # print(result_irdent)
  # print(result_sum)
  connection.close()

  irdent = []
  for data in result_irdent:
    row = {
      'idn': data[0],
      'num': data[1]
    }
    irdent.append(row)

  # print(irdent)

  sum = []
  for data in result_sum:
    row2 = {
      'add': data[0]
    }
    sum.append(row2)

  print(irdent + sum)

  return render(request, 'main/third.html',{"irdent":irdent,"sum":sum})


