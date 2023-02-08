from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Modelo para reservarexposicoes

class Exposicao(models.Model):
    titulo = models.CharField(max_length=300)
    descricao = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.titulo)

class Reserva(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    exposicao = models.ForeignKey(Exposicao, on_delete = models.CASCADE, null = True, blank = True)
    dataEntrada = models.DateField(verbose_name = 'Data de entrada', help_text = 'Utilize o formato AAAA-MM-DD')
    dataSaida =  models.DateField(verbose_name = 'Data de saída', help_text = 'Utilize o formato AAAA-MM-DD')
    horarioEntrada = models.TimeField(verbose_name = 'Horário de entrada', help_text = 'Utilize o formato HH:MM')
    horarioSaida = models.TimeField(verbose_name = 'Horário de saída', help_text = 'Utilize o formato HH:MM')

    def __str__(self):
        return str(self.user) + ' - ' + str(self.exposicao) + ' - ' + str(self.dataEntrada)
