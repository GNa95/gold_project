from django.shortcuts import render
from main.models import TbEnt # Post 모델 불러오기
from django.core import serializers
import json
from django.db.models import Q
from user.decorators import login_required

# Create your views here.
@login_required
def martSearch(request):
  kw = request.GET.get('kw') #검색어
  tb_ent = TbEnt.objects.order_by('ent_num')
  if kw:
    tb_ent = tb_ent.filter(
      Q(ent_addr__icontains=kw) |
      Q(ent_nm__icontains=kw)
    ).distinct()
  ent_json = serializers.serialize('json',tb_ent)
  ents = json.loads(ent_json)
  ent_list = []
  for ent in ents:
    ent_list.append(ent['fields'])
  entJson = json.dumps(ent_list, ensure_ascii=False)
  login_session = request.session.get('login_session', '')
  return render(request, 'mart/search.html',{"ent_list":entJson, "login_session":login_session})
  
