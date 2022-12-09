import urllib.request
# import requests
from bs4 import BeautifulSoup
import time
from django.db import connection


def crawl(good, ent):
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getProductPriceInfoSvc.do?'
    decode = "serviceKey=ZeM/dP8iYPl9QApaVhY+2H8bq1oTEhFfyXGRbF+PyFqCgxa+oclNYnWH2GPpt1I5/F1XaxF3reAG/YL0QLvsTQ=="
    encode = "serviceKey=ZeM%2FdP8iYPl9QApaVhY%2B2H8bq1oTEhFfyXGRbF%2BPyFqCgxa%2BoclNYnWH2GPpt1I5%2FF1XaxF3reAG%2FYL0QLvsTQ%3D%3D"

    date = [20221118, 20221104, 20221021, 20221007, 20220923, 20220902, 20220819]
    # good =[1072, 248, 945, 5035, 5141, 5013, 5140, 856, 5217, 1225]
    # ent = [1276, 1410, 1409]
    
    result = {}
    cursor = connection.cursor()
    for i, j in enumerate(ent):
        entpId = '&entpId=%d'%j
        good_dict = {}
        sql = "select gd_num, sale_price "+ \
            " from tb_user a join tb_ent b on a.username = b.ent_nm "+ \
            "              join th_sale c on a.user_id = c.user "+ \
            "              join th_saled d on c.id = d.sale_id  "+ \
            "             join tb_gds e on d.sale_gds = e.gd_nm "+ \
            " where ent_num = '" + str(j) + "' and gd_num in (" + ",".join(map(str,good)) +") "+ \
            "  and start_date <= sysdate() and end_date >= sysdate();"
        cursor.execute(sql)
        db_result = dictfetchall(cursor)
        for data in db_result:
            good_dict[data['gd_num']] = data['sale_price']
        if len(good_dict) != len(good):
            for k in date:
                goodInspectDay = '&goodInspectDay=%d'%k
                data = urllib.request.Request(url+decode+goodInspectDay+entpId)
                time.sleep(0.1)
                text = urllib.request.urlopen(url=data, timeout=2).read()
                soup = BeautifulSoup(text, 'lxml')

                if soup.select_one('resultcode').string == '90':
                    data = urllib.request.Request(url+encode+goodInspectDay+entpId)
                    text = urllib.request.urlopen(url=data,timeout=2).read()
                    soup = BeautifulSoup(text, 'lxml')

                items = soup.find_all("iros.openapi.service.vo.goodpricevo")
                if items:
                    break

            for item in items:
                # entpid = item.find("entpid").string
                goodid = int(item.find("goodid").string)
                goodprice = item.find("goodprice").string
                if (goodid in good) and (goodid not in good_dict):
                    good_dict[goodid] = goodprice 
                    
            result['mart'+str(i+1)] = good_dict
        else:
            pass
    connection.close()
    return result



def dictfetchall(cursor):
  columns = [col[0] for col in cursor.description]
  return [
    dict(zip(columns, row))
    for row in cursor.fetchall()
  ]