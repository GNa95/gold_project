from django.contrib import admin
from .models import *
# from .models import User

# Register your models here.

admin.site.register(secinquiry)
#admin.site.register(User)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         'user_id',
#         # 'user_pw',
#         'username',
#         #'is_superuser',
#         'user_phone',
#         #'user_gender',
#         #'user_birth',
#         'user_addr',
        
#     )
    # list_display_links = (
    #     'user_id',
    #     'username',
    # )