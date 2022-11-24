from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('',views.index, name="index"),
    path('second/',views.second, name="second"),
    path('third/',views.third, name="third")
]