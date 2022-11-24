from django.urls import path
from . import views

app_name = 'mart'

urlpatterns = [
    path('',views.martSearch, name="martSearch"),
]