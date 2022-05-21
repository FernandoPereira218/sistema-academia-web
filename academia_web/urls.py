"""academia_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_page),
    path('teste/', views.teste_db),
    path('login/submit', views.submit_login),
    path('principal/', views.main_page),
    path('', RedirectView.as_view(url='/login/')),
    path('cadastro/', views.add_user),
    path('cadastro/submit_user', views.submit_user),
    path('logout/', views.logout_user),
    path('cadastro_aluno/', views.cadastrar_aluno),
    path('cadastro_aluno/submit_aluno', views.submit_aluno),
    path('consulta_aluno/', views.consultar_aluno),
    path('consulta_aluno/<id_aluno>', views.buscar_aluno),
    path('consulta_aluno/<id_aluno>/criar_treino', views.criar_treino),
    path('consulta_aluno/<id_aluno>/criar_treino/submit', views.submit_treino),
    path('consulta_aluno/<id_aluno>/alterar_treino', views.alterar_treino),
    path('consulta_aluno/<id_aluno>/alterar_treino/submit', views.submit_alterar_treino),
]
