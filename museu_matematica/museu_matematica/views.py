from django.shortcuts import render
from django.forms.forms import Form
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User

from museu_matematica.models import Reserva
from museu_matematica.forms import ReservaModel2Form
from museu_matematica.forms import ReservaModel2FormCreate

from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class ReservaLoginView(LoginView):
    template_name = 'museu_matematica/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("museu_matematica:reservas-exibe")

class ReservaRegisterPage(FormView):
    template_name = 'museu_matematica/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("museu_matematica:reservas-exibe")

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)
        return super(ReservaRegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("museu_matematica:reservas-exibe")
        return super(ReservaRegisterPage, self).get(*args, **kwargs)

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
    template_name = 'museu_matematica/reserva.html'
    context_object_name = 'reservas'
    success_url = reverse_lazy("museu_matematica:reservas-exibe")

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

class ReservaCreate(LoginRequiredMixin, CreateView):
    model = Reserva
    template_name = 'museu_matematica/reserva_criar.html'
    context_object_name = 'reserva'
    fields = ['dataEntrada', 'dataSaida', 'horarioEntrada', 'horarioSaida']
    success_url = reverse_lazy("museu_matematica:reservas-exibe") # Após post submetido

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ReservaCreate, self).form_valid(form)

        
class ReservaUpdate(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs): # Busca os dados de uma reserva e exibe como um formulário
        reserva = Reserva.objects.get(pk=pk)
        formulario = ReservaModel2FormCreate(instance=reserva)
        context = {'form': formulario, } # Coloca o registro recuperado do banco e coloca num formulário
        return render(request, 'museu_matematica/reserva_editar.html', context)

    def post(self, request, pk, *args, **kwargs): # Recebe os dados de uma reserva e atualiza o banco de dados
        reserva = get_object_or_404(Reserva, pk=pk) # Pega a reserva ou retorna erro 404
        formulario = ReservaModel2FormCreate(request.POST, instance=reserva)
        if formulario.is_valid():
            contato = formulario.save()
            contato.save()
            return HttpResponseRedirect(reverse_lazy("museu_matematica:reservas-exibe"))
        else:
            context = {'formulario': formulario, } # Coloca o registro recuperado e coloca num formulário
            return render(request, 'museu_matematica/reserva_criar.html', context)

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

def exposicoes(request):
    return render(request, 'museu_matematica/reservas.html')

def login(request):
    return render(request, 'museu_matematica/login.html')

def reservar(request):
    return render(request, 'museu_matematica/reserva_exposicao.html')
