from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name="login"),
    path('painel_teste/', views.painel_teste, name='painel_teste'),
    path('logout/', views.logout_view, name='logout'),
]