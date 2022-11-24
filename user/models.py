from django.db import models
#from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

# USER_ROLES = {
#     'ROLE_NOMAL' : 'NORMAL',
#     'ROLE_COMPANY' : 'COMPANY',
#     'ROLE_SUPER' : 'SUPER'
# }

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=40, verbose_name='유저 전화번호')
    user_addr = models.CharField(max_length=40, verbose_name='유저 주소')
    user_level =models.CharField(max_length=8 ,verbose_name="등급")



    def __str__(self): #2
        return self.user_name
    
    class Meta: #3
        db_table = 'TB_USER'
        verbose_name = '유저'
        verbose_name_plural = '유저'
    
    

#일반 사용자 생성







class secinquiry(models.Model):
    inquirys_name = models.CharField(max_length=20)
    inquirys_email = models.CharField(max_length=30)
    inquirys_text = models.TextField(max_length=500)