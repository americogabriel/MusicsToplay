from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import MusicasAprender,MusicasAprendidas
from django.views.generic import View,CreateView,ListView,UpdateView,DeleteView,DetailView
import requests #biblioteca para requisições http, vamos usar para fazer requisições na nossa api do deezer
from django.http import HttpResponse

# pagina Home/listagem dos resultados 
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
       
# view para visualizar detalhes de uma musica da requisição à API Deezer
class PerfilMusica(View):
    def get(self,request,*args,**kwargs):
        query = kwargs.get('id') # pego o id da musica que foi enviado pela url e armazenado no kwargs da requisição(exemplo -> {'id':21312}) 
        response = requests.get(f"https://api.deezer.com/track/{query}")
        context = {}
        context['musica'] = response.json()
        # acessa o dicionário musica e sua chave 'bpm'
        context['musica']['bpm'] = float(context['musica']['bpm'])# alterando o valor de bpm de string para float
        context['musica']['bpm'] = round(int(context['musica']['bpm'])) # alterando de float para int e arredondando o valor
        return render(request,'cifras/perfilmusica.html',context)
    
#------------ VIEWS PARA MODEL MusicasAprender ------------

# view que cria um objeto "MusicasAprender"
class CreateMusicasAprender(View):
    def post(self,request,*args,**kwargs):
        id_musica = request.POST.get('id_musica')
        capa_album = request.POST.get('imagem_album')
        nome_banda = request.POST.get('nome_banda')
        nome_musica = request.POST.get('nome_musica')
        duracao = request.POST.get('duracao')
        bpm = float(request.POST.get('bpm')) # o campo bpm chega como uma string que guarda um número decimal e nós transformamos em float
        bpm = round(bpm) # aqui pegamos esse float e arredondamos para cima, tornando ela um INT(nosso campo "bpm" do model só aceita valores inteiros)
        instrumento = request.POST.get('instrumento')

        obj = MusicasAprender.objects.create(capa_album = capa_album,nome_banda = nome_banda,nome_musica = nome_musica, duracao = duracao, bpm = bpm, instrumento = instrumento)
        if obj:
            return redirect("url_perfilmusica",id = id_musica)
        
# View para listar todos os objetos "MusicasAprender"        
class ListMusicasAprender(ListView):
    model = MusicasAprender
    context_object_name = "musicas_aprender"
    template_name = 'cifras/listmusicas.html'

    # método da class based view usado para manipular o objeto enviado para o template, usado normalmente em views de listagem de objetos
    def get_queryset(self):
        # recebe pela URL no metodo GET a string do instrumento para filtrar a busca
        query = self.request.GET.get('q')
        if query:
            return MusicasAprender.objects.filter(instrumento = query) # Se o programa encontrar o filtro no metodo GET do request(informação pela url do site) ele retorna os objetos com instrumento igual à palavra encontrada no GET
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = "MusicasAprender"

        return context

# para atualizar o objeto "MusicasAprender"
class UpdateMusicasAprender(UpdateView):
    model = MusicasAprender
    fields = ['nome_banda','nome_musica','duracao','bpm','instrumento']
    template_name = 'cifras/updateMusicas.html'
    success_url = reverse_lazy('url_listmusicas')

# view para detalhes de um objeto "MusicasAprender"
class PerfilMusicaAprender(DetailView):
    model = MusicasAprender
    template_name = 'cifras/perfilmusicasaprender.html'
    context_object_name = "musica"

# View para deletar um objeto específico "MusicasAprender"
class DeleteMusicasAprender(DeleteView):
    model = MusicasAprender
    template_name = 'cifras/deletemusicas.html'
    success_url = reverse_lazy('url_listmusicas')

#------------ Views para model MusicasAprendidas ------------

# para criar um objeto MusicasAprendida
class CreateMusicasAprendidas(View):
    def post(self,request,*args,**kwargs):
        id_musica = request.POST.get('id_musica')
        dominio_musica = request.POST.get('dominio')

        obj = MusicasAprendidas.objects.create(musica = get_object_or_404(MusicasAprender,pk = id_musica), dominio = dominio_musica)

        if obj:
            return redirect('url_listmusicasaprender')

# para lista os objetos do model MusicasAprendida
class ListMusicasAprendidas(ListView):
    model = MusicasAprendidas
    template_name = "cifras/listmusicas.html"
    context_object_name = 'musicas_aprendidas'


    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return MusicasAprendidas.objects.filter(musica__instrumento = query) # em Django, usamos duas underlines("__") para acessar campos do objeto referenciado numa ForeignKey, no nosso caso queremos acesso ao campo instrumento do objeto "MusicasAprender" que é referenciado no campo musica do model "MusicasAprendidas" na ForeignKey "musica"
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = "MusicasAprendidas"

        return context


class PerfilUser(View):
    def get(self,request,*args,**kwargs):
        if request.GET.get('filtro') == "musicasaprendidas":
            return redirect('url_listmusicasaprendidas')
        elif request.GET.get('filtro') == "musicasaprender":
            return redirect('url_listmusicasaprender')

        return render (request,"cifras/perfil.html")
