from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from .models import MainBoard, Reply
from main.models import TbEntArea
#from user.models import User
from django.utils import timezone
from .forms import WriteForm, ReplyForm
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

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

  context = {'board_list': page_obj, 'page': page, 'kw': kw, 'area_text': area_text, 'all_area': all_area}
  return render(request, 'community/board.html', context)


    


'''특정 게시글 클릭 시 게시글 속으로 들어가는 기능'''
def board_detail(request, board_id):
  board = get_object_or_404(MainBoard, pk=board_id)
  comment = ReplyForm()
  comment_view = Reply.objects.filter(post=board_id)
  context = {'board': board, 'comment':comment, 'comment_view':comment_view}
  return render(request, 'community/board_detail.html', context)


'''게시글에 대한 댓글 기능'''
def reply_create(request, board_id):
  reply_create = ReplyForm(request.POST)
  #user_id = request.session['user']
  #user = User.objects.get(pk=user_id)
  if reply_create.is_valid():
    reply = reply_create.save(commit=False)
    reply.post = get_object_or_404(MainBoard, pk=board_id)
    #reply.author = user
    reply.save()
  return redirect('community:board_detail', board_id)


'''게시글 작성 기능'''
def board_create(request):
  #if not request.session.get('User.user'):
    #return redirect('user:login')

  if request.method == 'POST':
    form = WriteForm(request.POST)
    if form.is_valid():
      #user_id = request.session.get('User.user')
      #user = User.objects.get(pk=user_id)

      board = MainBoard()
      board.title = form.cleaned_data['title']
      board.content = form.cleaned_data['content']
      #board.writer = user
      board.created_dt = timezone.now()
      board.save()
      return redirect('community:board_list')
  else:
    form = WriteForm()
  context = {'form': form}
  return render(request, 'community/board_write.html', context)


