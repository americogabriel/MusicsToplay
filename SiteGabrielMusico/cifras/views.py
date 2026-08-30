from django.shortcuts import render
from django.urls import reverse_lazy
from .models import MusicasAprender
from django.views.generic import View,CreateView,ListView,UpdateView,DeleteView,FormView
import requests #biblioteca para requisições http, vamos usar para fazer requisições na nossa api do deezer
from django.http import HttpResponse
import json


class Home(View):
    def get(self,request,*args,**kwargs):
        
        return render(request,"cifras/home.html")
    
    def post(self,request,*args,**kwargs):

        # quando enviar a pesquisa e o request receber pelo método POST a pesquisa, ele pega adiciona a pesquisa na API
        query = request.POST.get('pesquisa')
        response = requests.get(f"https://api.deezer.com/search?q={query}")

        # cria um contexto que contém a resposta da API com o resultado da busca, e através do render envia elas para o template renderizar
        context = {}
        context['musicas'] = response.json() # pega a resposta retornada pela API em formato JSON e transforma ela em algum tipo python(lista,dicionario,string,etc) para facilitar a manipulçao do arquivo json, no nosso caso foi transformado em um dicionario
        context['method'] = request.method
        print(context['musicas']['data'][0])
        return render(request,"cifras/home.html",context)






class CreateMusicasAprender(CreateView):
    model = MusicasAprender
    fields = ['nome_banda','nome_musica','duracao','tom_musica','instrumento']
    template_name = 'cifras/createMusicasAprender.html'
    success_url = reverse_lazy('url_home')

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
