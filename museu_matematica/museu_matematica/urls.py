"""museu_matematica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from museu_matematica.views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.urls.base import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('exposicoes/', ExposicaoListView.as_view(), name='exposicoes'),
    path('adicionar-exposicao/', ExposicaoCreate.as_view(), name='exposicao-create'),
    path('deletar-exposicao/<int:pk>', ExposicaoDelete.as_view(), name='exposicao-delete'),
    path('editar-exposicao/<int:pk>', ExposicaoUpdate.as_view(), name='exposicao-editar'),
    path('reservar/<int:pk>', ReservaCreateView.as_view(), name='reservar'),
    path('lista-reservas/', ReservaListView.as_view(), name="lista-reservas"),
    path('editar-reserva/<int:pk>', ReservaUpdate.as_view(), name="reserva-editar"),
    path('reserva-delete/<int:pk>', ReservaDelete.as_view(), name="reserva-delete"),
    path('accounts/login/', LoginView.as_view(template_name="museu_matematica/login.html"), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page = reverse_lazy('homepage')), name='logout'),
    path('accounts/registro/', registro, name = 'registro'),
    path("reserva-ajax", verificaReserva, name = 'reserva-ajax'),
]

app_name = 'museu_matematica'

