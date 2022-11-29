from django import forms
from .models import User, ThSale
from argon2 import PasswordHasher, exceptions
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=32,
        label='아이디',
        widget=forms.TextInput(
        ),
        error_messages={'required' : '아이디를 입력하세요.'}
    )

    password = forms.CharField(
        max_length=128,
        label='비밀번호',
        widget=forms.PasswordInput,
        error_messages={'required' : '비밀번호를 입력하세요.'}
    )

    field_order = [
        'user_id',
        'password'
    ]

    def clean(self):
        cleaned_data = super().clean()
 
        user_id = cleaned_data.get('user_id', '')
        password = cleaned_data.get('password', '')
        if user_id and password :
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                print("아이디 없음")
                return self.add_error('user_id', '아이디가 존재하지 않습니다.')

            try:
                PasswordHasher().verify(user.password, password)
            except exceptions.VerifyMismatchError:
                print("비번 없음")
                return self.add_error('password', '비밀번호가 다릅니다.')
            
            self.login_session = user.user_id


class SaleForm(forms.ModelForm):
    class Meta:
        model = ThSale
        fields = ['sale_name','start_date', 'end_date']
