from django.db import models
from user.models import User


'''게시글(MainBoard) 모델'''

class MainBoard(models.Model):
    AREA_CHOICES = (
        ('20100000', '서울특별시'), ('20120000', '강남구'), ('20112000', '강동구'), ('20103000', '강북구'), ('20110000', '강서구'), ('20124000', '관악구'),
        ('20113000', '광진구'), ('20123000', '구로구'), ('20125000', '금천구'), ('20102000', '노원구'), ('20101000', '도봉구'), ('20109000', '동대문구'),
        ('20122000', '동작구'), ('20111000', '마포구'), ('20108000', '서대문구'), ('20121000', '서초구'), ('20114000', '성동구'), ('20105000', '성북구'),
        ('20119000', '송파구'), ('20118000', '양천구'), ('20116000', '영등포구'), ('20117000', '용산구'), ('20104000', '은평구'), ('20106000', '종로구'),
        ('20115000', '중구'), ('20107000', '중랑구')
    )
    area = models.CharField(max_length=8, choices=AREA_CHOICES, default='20122000')
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(max_length=1000, blank=False)
    writer = models.CharField(max_length=50)
    created_dt = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '커뮤니티'
        verbose_name_plural = '커뮤니티'
        db_table = 'tb_mainboard'


'''댓글(Reply) 모델'''

class Reply(models.Model):
    reply = models.TextField()
    author = models.CharField(max_length=50)
    board = models.ForeignKey('MainBoard', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.reply
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
        db_table = 'tb_reply'





