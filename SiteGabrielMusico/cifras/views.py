from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import MusicasAprender
from django.views.generic import View,CreateView,ListView,UpdateView,DeleteView,FormView
import requests #biblioteca para requisições http, vamos usar para fazer requisições na nossa api do deezer
from django.http import HttpResponse

class Home(View):
    # usa somente o method GET e usa o if para indentificar se é uma requisição com pesquisa enviada ou o usuário está na tela inicial de pesquisa
    def get(self,request,*args,**kwargs):
        
        if request.GET.get('pesquisa'):
            # quando enviar a pesquisa e o request receber pelo método POST a pesquisa, ele pega adiciona a pesquisa na API
            query = request.GET.get('pesquisa')
            response = requests.get(f"https://api.deezer.com/search?q={query}")

            # cria um contexto que contém a resposta da API com o resultado da busca, e através do render envia elas para o template renderizar
            context = {}
            context['musicas'] = response.json() # pega a resposta retornada pela API em formato JSON e transforma ela em algum tipo python(lista,dicionario,string,etc) para facilitar a manipulçao do arquivo json, no nosso caso foi transformado em um dicionario
            return render(request,"cifras/home.html",context)
        else:
            # renderiza somente o template da barra de pesquisa
            return render(request,"cifras/home.html")

class PerfilMusica(View):
    def get(self,request,*args,**kwargs):
        query = kwargs.get('id') # pego o id da musica que foi enviado pela url e armazenado no kwargs da requisição(exemplo -> {'id':21312}) 
        response = requests.get(f"https://api.deezer.com/track/{query}")
        context = {'musica' : response.json()}
        return render(request,'cifras/perfilmusica.html',context)
    


class CreateMusicasAprender(View):
    def post(self,request,*args,**kwargs):
        id_musica = request.POST.get('id_musica')
        nome_banda = request.POST.get('nome_banda')
        nome_musica = request.POST.get('nome_musica')
        duracao = request.POST.get('duracao')
        bpm = float(request.POST.get('bpm')) # o campo bpm chega como uma string que guarda um número decimal e nós transformamos em float
        bpm = round(bpm) # aqui pegamos esse float e arredondamos para cima, tornando ela um INT(nosso campo "bpm" do model só aceita valores inteiros)
        instrumento = request.POST.get('instrumento')

        obj = MusicasAprender.objects.create(nome_banda = nome_banda,nome_musica = nome_musica, duracao = duracao, bpm = bpm, instrumento = instrumento)
        if obj:
            return redirect("url_perfilmusica",id = id_musica)
    

class UpdateMusicasAprender(UpdateView):
    model = MusicasAprender
    fields = ['nome_banda','nome_musica','duracao','tom_musica','instrumento']
    template_name = 'cifras/updateMusicas.html'
    success_url = reverse_lazy('url_listmusicas')

class ListMusicasAprender(ListView):
    model = MusicasAprender
    context_object_name = "musicas"
    template_name = 'cifras/listmusicas.html'

    # método da class based view usado para manipular o objeto enviado para o template, usado normalmente em views de listagem de objetos
    def get_queryset(self):
        # recebe pela URL no metodo GET a string do instrumento para filtrar a busca
        query = self.request.GET.get('q')
        if query:
            return MusicasAprender.objects.filter(instrumento = query) # Se o programa encontrar o filtro no metodo GET do request(informação pela url do site) ele retorna os objetos com instrumento igual à palavra encontrada no GET
        return super().get_queryset()

class DeleteMusicasAprender(DeleteView):
    model = MusicasAprender
    template_name = 'cifras/deletemusicas.html'
    success_url = reverse_lazy('url_listmusicas')
