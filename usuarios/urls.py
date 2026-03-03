from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_opcoes, name='opcoes'),
    path('login/', views.login_usuario, name='login'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('painel/', views.home, name='home'),
    path('home_admin/', views.home_admin, name='home_admin'),
    path('adicionar_quarto/', views.adicionar_quarto, name='adicionar_quarto'),
    path('editar_quarto/<int:quarto_id>/', views.editar_quarto, name='editar_quarto'),
    path('remover_quarto/<int:quarto_id>/', views.remover_quarto, name='remover_quarto'),
    path('sair/', views.logout_usuario, name='logout'),
]
