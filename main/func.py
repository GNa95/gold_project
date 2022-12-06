import urllib.request
# import requests
from bs4 import BeautifulSoup
import time
from django.db import connection

def crawl(good, ent):
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getProductPriceInfoSvc.do?'
    serviceKey = "serviceKey=sUIo/mwzlBQJ/rIBdqyj5SXiXUxaOrRv6H+ZpNgJ1URCmNPNQMlC5imaW7yE4lngVBxrRcW/3TNbtSsoCGvLhg"

    date = [20221118, 20221104, 20221021, 20221007, 20220923, 20220902, 20220819]
    # good =[1072, 248, 945, 5035, 5141, 5013, 5140, 856, 5217, 1225]
    # ent = [1276, 1410, 1409]
    result = {}
    cursor = connection.cursor()
    for j in good:
        goodId = '&goodId=%d'%j 
        good_dict = {}
        for h, k in enumerate(ent):
            entpId = '&entpId=%d'%k
            sql = "select sale_price "+ \
                  " from tb_user a join tb_ent b on a.username = b.ent_nm "+ \
                  "              join th_sale c on a.user_id = c.user "+ \
                  "              join th_saled d on c.id = d.sale_id  "+ \
                  "             join tb_gds e on d.sale_gds = e.gd_nm "+ \
                  " where ent_num = '" + str(k) + "' and gd_num = '" + str(j) +"' " \
                  "  and start_date <= sysdate() and end_date >= sysdate();"
            cursor.execute(sql)
            db_result = cursor.fetchall()
            if db_result:
                goodprice = int(db_result[0][0])
            else:
                for i in date:
                    goodInspectDay = '==&goodInspectDay=%d'%i
                    data = urllib.request.Request(url+serviceKey+goodInspectDay+entpId+goodId)
                    # data = requests.get(url+serviceKey+goodInspectDay+entpId+goodId)
                    time.sleep(0.1)
                    text = urllib.request.urlopen(data).read()
                    soup = BeautifulSoup(text, 'lxml')
                    try:
                        # goodinspectday = soup.select_one("goodinspectday").string
                        # entpid = soup.select_one("entpid").string
                        # goodid = soup.select_one("goodid").string
                        goodprice = soup.select_one("goodprice").string
                        goodprice = int(goodprice)
                        break
                    except:
                        goodprice= None
            good_dict['mart'+str(h+1)] = goodprice
        result[j] = good_dict
    connection.close()
    return result



def dictfetchall(cursor):
  columns = [col[0] for col in cursor.description]
  return [
    dict(zip(columns, row))
    for row in cursor.fetchall()
  ]