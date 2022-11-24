from django.db import models
#from user.models import user

'''게시글(MainBoard) 모델'''
class MainBoard(models.Model):
    AREA_CHOICES = (
        ('20100000', '서울전체'), ('20120000', '강남'), ('20112000', '강동'), ('20103000', '강북'), ('20110000', '강서'), ('20124000', '관악'),
        ('20113000', '광진'), ('20123000', '구로'), ('20125000', '금천'), ('20102000', '노원'), ('20101000', '도봉'), ('20109000', '동대문'),
        ('20122000', '동작'), ('20111000', '마포'), ('20108000', '서대문'), ('20121000', '서초'), ('20114000', '성동'), ('20105000', '성북'),
        ('20119000', '송파'), ('20118000', '양천'), ('20116000', '영등포'), ('20117000', '용산'), ('20104000', '은평'), ('20106000', '종로'),
        ('20115000', '중구'), ('20107000', '중랑')
    )
    area = models.CharField(max_length=8, choices=AREA_CHOICES, default='20122000')
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(max_length=1000, blank=False)
    #writer = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '커뮤니티'
        verbose_name_plural = '커뮤니티'


'''댓글(Reply) 모델'''

class Reply(models.Model):
    reply = models.TextField()
    #author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('MainBoard', null=True, blank=True, on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.reply
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글'




