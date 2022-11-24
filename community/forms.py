from django import forms
from .models import  Reply

class WriteForm(forms.Form):
    title = forms.CharField(
        error_messages={'required': '제목을 입력하세요'},
        max_length=64,
        label='제목')
    content = forms.CharField(
        error_messages={'required': '내용을 입력하세요'},
        widget=forms.Textarea,
        label='내용')
    # tags = forms.CharField(required=False, label='태그')

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']
        labels = {'reply': '댓글 내용'}


