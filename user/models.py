from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

# USER_ROLES = {
#     'ROLE_NOMAL' : 'NORMAL',
#     'ROLE_COMPANY' : 'COMPANY',
#     'ROLE_SUPER' : 'SUPER'
# }

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    user_id = models.CharField(max_length=50, unique=True)
    user_phone = models.CharField(max_length=40, verbose_name='유저 전화번호')
    user_addr = models.CharField(max_length=40, verbose_name='유저 주소')
    user_level =models.CharField(max_length=8 ,verbose_name="등급")

    def __str__(self): #2
        return self.user_id
    
    class Meta: #3
        db_table = 'TB_USER'
        verbose_name = '유저'
        verbose_name_plural = '유저'
    
    


# 문의하기 Table
class secinquiry(models.Model):
    inquirys_name = models.CharField(max_length=20)
    inquirys_email = models.CharField(max_length=30)
    inquirys_text = models.TextField(max_length=500)

    class Meta: #3
        db_table = 'TB_inquiry'


# sale이력 Table
class ThSale(models.Model):
    sale_name = models.CharField(max_length=30)
    user = models.CharField(max_length=20)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sale_name

    class Meta: #3
        db_table = 'TH_SALE'

class ThSaleDetail(models.Model):
    sale = models.ForeignKey('ThSale', on_delete=models.CASCADE)
    gd_type_cd = models.CharField(max_length=10)
    sale_gds = models.CharField(max_length=100)
    sale_price = models.IntegerField()

    class Meta:
        db_table = 'TH_SALED'
        