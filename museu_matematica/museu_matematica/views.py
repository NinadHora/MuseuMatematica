from django.shortcuts import render
from django.forms.forms import Form
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User

from museu_matematica.models import Reserva, Exposicao
from museu_matematica.forms import ReservaModel2Form
from museu_matematica.forms import ReservaModel2FormCreate

from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class ExposicaoListView(View):
    def get(self, request, *args, **kwargs):
        exposicoes = Exposicao.objects.all()
        context = { 'exposicoes': exposicoes, }
        return render(request, 'museu_matematica/exposicoes.html', context)

def verificaReserva(request):
    search_input_hrEntrada = request.GET.get('hrEntrada')
    search_input_hrSaida = request.GET.get('hrSaida')
    search_input_dtEntrada = request.GET.get('dtEntrada')
    search_input_dtSaida = request.GET.get('dtSaida')
    
    print(request)

    if(search_input_hrEntrada == search_input_hrSaida and search_input_dtEntrada == search_input_dtSaida and search_input_hrEntrada != ""):
        resposta = {
                'hrIgual':
                    'True'}
        return JsonResponse(resposta)
    else:
        resposta = {
                'hrIgual':
                    'False'}
        return JsonResponse(resposta)


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'museu_matematica/lista-reservas.html'
    context_object_name = 'reservas'
    success_url = reverse_lazy("lista-reservas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['reservas'] = context['reservas'].filter(user = self.request.user) # Apenas os itens do usuário logado

        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['reservas'] = context['reservas'].filter(dataEntrada__exact=search_input)
            
        

        context['search_input'] = search_input
        print(context)
        

        return context
        

class ReservaDetail(LoginRequiredMixin, CreateView):
    def get(self, request, pk, *args, **kwargs):
        reserva = Reserva.objects.get(pk=pk)
        context = { 'reserva': reserva }
        return render(request, 'museu_matematica/reserva_detalhes.html', context)

    def post(self, request, *args, **kwargs):
        pass

class ReservaCreateView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {
            'exposicao': Exposicao.objects.get(pk=pk),
            'formulario': ReservaModel2FormCreate, 
            }
        return render(request, "museu_matematica/reserva_exposicao.html", context) 
    def post(self, request, pk, *args, **kwargs):
        formulario = ReservaModel2FormCreate(request.POST)
        if formulario.is_valid():
            reserva = formulario.save()
            reserva.user = self.request.user
            reserva.exposicao = get_object_or_404(Exposicao, pk=pk)
            reserva.save()
            return HttpResponseRedirect(reverse_lazy("homepage"))

class ReservaCreate(LoginRequiredMixin, CreateView):
    model = Reserva
    template_name = 'museu_matematica/reserva_criar.html'
    context_object_name = 'reserva'
    fields = ['dataEntrada', 'dataSaida', 'horarioEntrada', 'horarioSaida']
    success_url = reverse_lazy("museu_matematica/reservas-exibe") # Após post submetido

    def form_valid(self, form, exposicao):
        form.instance.user = self.request.user
        form.instance.exposicao = Exposicao.objects.get(pk = exposicao)
        return super(ReservaCreate, self).form_valid(form)

        
class ReservaUpdate(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs): # Busca os dados de uma reserva e exibe como um formulário
        reserva = Reserva.objects.get(pk=pk)
        formulario = ReservaModel2FormCreate(instance=reserva)
        context = {'form': formulario, } # Coloca o registro recuperado do banco e coloca num formulário
        return render(request, 'museu_matematica/reserva-editar.html', context)

    def post(self, request, pk, *args, **kwargs): # Recebe os dados de uma reserva e atualiza o banco de dados
        reserva = get_object_or_404(Reserva, pk=pk) # Pega a reserva ou retorna erro 404
        formulario = ReservaModel2FormCreate(request.POST, instance=reserva)
        if formulario.is_valid():
            contato = formulario.save()
            contato.save()
            return HttpResponseRedirect(reverse_lazy("lista-reservas"))
        # else:
            # context = {'formulario': formulario, } # Coloca o registro recuperado e coloca num formulário
            # return render(request, 'museu_matematica/reserva_criar.html', context)
            

class ReservaDelete(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        reserva = Reserva.objects.get(pk=pk)
        context = { 'reserva': reserva }
        return render(request, 'museu_matematica/reserva_confirmar_deletar.html', context)

    def post(self, request, pk, *args, **kwargs):
        reserva = Reserva.objects.filter(pk=pk).delete()
        return HttpResponseRedirect(reverse_lazy("museu_matematica:reservas-exibe"))

# Create your views here.
def homepage(request):
    return render(request, 'museu_matematica/index.html')

def login(request):
    return render(request, 'museu_matematica/login.html')

def reservar(request):
    return render(request, 'museu_matematica/reserva_exposicao.html')

def registro(request):
    if request.method == 'POST':
        # create user
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('homepage')
        else:
            context = {'form': formulario, }
        return render(request, 'museu_matematica/registro.html', context)
    else:
        # render form
        formulario = UserCreationForm()
    context = {'form': formulario, }
    return render(request, 'museu_matematica/registro.html')
