from django.urls import path

from . import views
from .views import CodeListView, CodeDetailView, CodeCreateView, CodeUpdateView, CodeDeleteView

urlpatterns = [
    path('', CodeListView.as_view(), name='index'),
    path('codes/<int:pk>/', CodeDetailView.as_view(), name='codeapp-code-detail'),
    path('codes/new/', CodeCreateView.as_view(), name='codeapp-code-create'),
    path('codes/<int:pk>/update/', CodeUpdateView.as_view(), name='codeapp-code-update'),
    path('codes/<int:pk>/delete/', CodeDeleteView.as_view(), name='codeapp-code-delete'),
    path('my_codes/', views.my_codes, name='codeapp-my-codes'),
]