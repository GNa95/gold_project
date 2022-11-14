from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    # email = forms.EmailField(label="이메일")
    phone = forms.CharField(label="핸드폰 번호")
    gender = forms.BooleanField(required=False)
    birth = forms.DateField(label="이메일")
    addr = forms.CharField(label="주소")
    class Meta:
        model = User
        fields = ("id","username","password1","password2","phone","gender","birth","addr")