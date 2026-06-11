from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cooperados, name='lista_cooperados'),
    path('novo/', views.criar_cooperado, name='criar_cooperado'),
    path('<int:pk>/', views.detalhe_cooperado, name='detalhe_cooperado'),
    path('<int:pk>/editar/', views.editar_cooperado, name='editar_cooperado'),
    path('<int:pk>/excluir/', views.excluir_cooperado, name='excluir_cooperado'),
]
