from django.urls import path
from . import views
from .views import CodeCreateView

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('code/new/', CodeCreateView.as_view(), name='code-create')
]