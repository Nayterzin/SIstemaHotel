from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_opcoes, name='opcoes'),
    path('login/', views.login_usuario, name='login'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('painel/', views.home, name='home'),
    path('sair/', views.logout_usuario, name='logout'),
]
