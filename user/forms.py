from django import forms
from .models import User
from argon2 import PasswordHasher, exceptions
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



# class UserForm(UserCreationForm):
#     # email = forms.EmailField(label="이메일")
#     user_id = forms.CharField(label="아이디")
#     user_phone = forms.CharField(label="핸드폰 번호",required=False)
#     user_addr = forms.CharField(label="주소", required=False)
#     class Meta:
#         model = get_user_model()
#         fields = ("user_id","username","password1","password2","user_phone","user_addr")

class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=32,
        label="아이디",
        # required=True,
        # widget=forms.TextInput(
        #     attrs={
        #         'class' : 'user_id',
        #         'placeholder' : '아이디'
        #     }
        # ),
        error_messages={'required' : '아이디를 입력'}
    )

    password = forms.CharField(
        max_length=128,
        label="비밀번호",
        #required=True,
        widget=forms.PasswordInput,
       #(
            # attrs={
            #     'class' : 'password',
            #     'placeholder' : '비밀번호'
            # }
        #),
        error_messages={'required' : '비밀번호를 입력'}
    )

    field_order = [
        'user_id',
        'password'
    ]

    def clean(self):
        cleaned_data = super().clean()
 
        user_id = cleaned_data.get('user_id', '')
        password = cleaned_data.get('password', '')
        if user_id == '':
            self.add_error('user_id', '아이디를 다시 입력')
        elif user_id == '':
            return self.add_error('password', '비밀번호를 다시 다시')
        else:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return self.add_error('user_id', '아이디가 존재 안한당')

            try:
                PasswordHasher().verify(user.password, password)
            except exceptions.VerifyMismatchError:
                return self.add_error('password', '비밀번호가 다르덩')
            
            self.login_session = user.user_id
