from django.db.models import fields
from django import forms
from museu_matematica.models import *

class ExposicaoModel2Form(forms.ModelForm):
    class Meta:
        model = Exposicao
        fields = '__all__'

class ReservaModel2Form(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

class ReservaModel2FormCreate(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['dataEntrada', 'dataSaida', 'horarioEntrada', 'horarioSaida']
