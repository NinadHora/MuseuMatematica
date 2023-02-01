from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'museu_matematica/index.html')

def exposicoes(request):
    return render(request, 'museu_matematica/reservas.html')

def login(request):
    return render(request, 'museu_matematica/login.html')

def reservar(request):
    return render(request, 'museu_matematica/reserva_exposicao.html')