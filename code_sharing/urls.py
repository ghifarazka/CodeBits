from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-Code'),
    path('mycodes/', views.mycodes, name='myCode-Code'),
]