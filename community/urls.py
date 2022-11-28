from django.urls import path
from . import views


app_name = 'community'

urlpatterns = [
    path('board/',views.board_list, name='board_list'),
    path('<int:board_id>/', views.board_detail, name='board_detail'),
    path('reply/create/<int:board_id>/', views.reply_create, name='reply_create'),
    path('board/create/', views.board_create, name='board_create'),
]
