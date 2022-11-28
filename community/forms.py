from django import forms
from .models import  MainBoard, Reply

class WriteForm(forms.ModelForm):
    class Meta:
        model = MainBoard
        fields = ['title', 'content', 'area']
        labels = {'title': '제목', 'content': '내용', 'area': '지역'}

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']
        labels = {'reply': '댓글 내용'}

        
# class SearchForm(forms.ModelForm):
#     class Meta:
#         model = Search
#         fields = ['keyword']
#         labels = {'keyword': '검색키워드'}


