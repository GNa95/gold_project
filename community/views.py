from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from .models import MainBoard, Reply
from main.models import TbEntArea
from user.models import User
from django.utils import timezone
from .forms import WriteForm, ReplyForm
from django.core.paginator import Paginator
from django.db.models import Q
from user.decorators import login_required

#Create your views here.

'''게시판 목록 출력 기능'''
def board_list(request):
  all_area = TbEntArea.objects.all()                            #지역 선택
  area_text = request.GET.get('area', '20100000')
  page = request.GET.get('page', '1')                           #페이지
  kw = request.GET.get('kw', '')                                #검색어
  board_list = MainBoard.objects.order_by('-created_dt')
  if kw:
    board_list = board_list.filter(
      Q(title__icontains=kw) |                                  #제목
      Q(content__icontains=kw)                                  #내용
  ).distinct()
  if area_text != '20100000':
    board_list = board_list.filter(
      Q(area__exact=area_text)
    ).distinct()
  
  paginator = Paginator(board_list, 10)                         #한 페이지당 10개씩 출력
  page_obj = paginator.get_page(page)

  area_text = int(area_text)
  login_session = request.session.get('login_session', '')
  context = {'board_list': page_obj, 'page': page, 'kw': kw, 'area_text': area_text, 'all_area': all_area, 'login_session': login_session}
  return render(request, 'community/board.html', context)  


'''특정 게시글 클릭 시 게시글 속으로 들어가는 기능'''
@login_required
def board_detail(request, board_id):
  board = get_object_or_404(MainBoard, pk=board_id)
  login_session = request.session.get('login_session', '')
  comments = ReplyForm()
  comment_view = Reply.objects.filter(board=board_id)
  context = {'board': board, 'comments': comments, 'comment_view': comment_view, 'login_session': login_session}
  return render(request, 'community/board_detail.html', context)


'''게시글에 대한 댓글 기능'''
@login_required
def reply_create(request, board_id):
  board = get_object_or_404(MainBoard, pk=board_id)
  login_session = request.session.get('login_session', '')
  if request.method == "POST":
    form = ReplyForm(request.POST)
    if form.is_valid():
      reply = form.save(commit=False)
      reply.create_dt = timezone.now()
      reply.board = board
      reply.author = login_session
      reply.save()
      return redirect('community:board_detail', board_id=board.id)
  else:
    return HttpResponseNotAllowed('Only POST is possible.')
  context = {'board': board, 'form': form, 'login_session': login_session}
  return render(request, 'community/board_detail.html', context)
  

'''게시글 작성 기능'''
@login_required
def board_create(request):
  login_session = request.session.get('login_session', '')
  if request.method == 'POST':
    form = WriteForm(request.POST)
    if form.is_valid():
      board = MainBoard()
      board.title = form.cleaned_data['title']
      board.content = form.cleaned_data['content']
      board.area = form.cleaned_data['area']
      board.created_dt = timezone.now()
      board.writer = login_session
      board.save()
      return redirect('community:board_list')
  else:
    form = WriteForm()
  context = {'form': form, 'login_session': login_session}
  return render(request, 'community/board_write.html', context)



