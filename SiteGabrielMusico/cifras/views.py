from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.urls import reverse,reverse_lazy
from .models import MusicasAprender,MusicasAprendidas
from django.views.generic import View,CreateView,ListView,UpdateView,DeleteView,DetailView,FormView
import requests #biblioteca para requisições http, vamos usar para fazer requisições na nossa api do deezer
from urllib.parse import urlencode 
from .forms import MusicaAprenderForm,MusicaAprendidaForm,CadastroUserForm,LoginUserForm
from django.contrib.auth.models import User
from django.http import HttpResponse


# TRATAR OS DADOS QUE CHEGAM DO FORMULÁRIO PARA CRIAR A CONTA
class Login(FormView):
    template_name = "cifras/login.html"
    form_class = LoginUserForm
    success_url = reverse_lazy('url_login')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['logando'] = True

        return context
    
    def form_valid(self, form):
        # acessa os campos enviados no form
        username = form.cleaned_data['username']
        senha = form.cleaned_data['password']

        acesso = authenticate(self.request,username = username,password = senha)

        if acesso:
            try:
                login(self.request,acesso)
                return redirect('url_home')
            except Exception as erro:
                return HttpResponse(f"{erro}")
        else:
            return super().form_invalid(form)  
         
        return super().form_valid(form)

class Cadastro(FormView):
    template_name = "cifras/login.html"
    form_class = CadastroUserForm
    success_url = reverse_lazy('url_login')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logando'] = False

        return context

    def form_valid(self,form):
        
        form.save()

        return super().form_valid(form)


# pagina Home/listagem dos resultados 
class Home(View):
    # usa somente o method GET e usa o if para indentificar se é uma requisição com pesquisa enviada ou o usuário está na tela inicial de pesquisa
    def get(self,request,*args,**kwargs):
        
        if request.GET.get('pesquisa') and request.GET.get('pagina'):
            # quando enviar a pesquisa e a página o request recebe pelo método GET, ele acessa os valores e faz a requisição
            pagina = request.GET.get('pagina')
            pesquisa = request.GET.get('pesquisa')
            response = requests.get(f"https://api.deezer.com/search?q={pesquisa}&index={pagina}")

            # cria um contexto que contém a resposta da API com o resultado da busca, e através do render envia elas para o template renderizar
            context = {}
            context['musicas'] = response.json() # pega a resposta retornada pela API em formato JSON e transforma ela em algum tipo python(lista,dicionario,string,etc) para facilitar a manipulçao do arquivo json, no nosso caso foi transformado em um dicionario

            # manda a pesquisa feita pelo usuário e a página atual em que se encontra os resultados para o template, para o botao de "proxima pagina" no template funcionar
            context['pesquisa'] = pesquisa
            context['pagina'] = int(pagina) # salva no contexto a pagina atual
            context['prox_pagina'] = int(pagina) + 25 # salva no contexto a proxima página
            context['pagina_anterior'] = int(pagina) - 25 # salva no contexto a página anterior

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

        # valores enviados pela query da URL
        context['pagina_musica'] = self.request.GET.get('pagina') # pega o valor pagina enviada pela query, que contém a página que o usuário estava antes de abrir a música
        context['pesquisa_user'] = self.request.GET.get('pesquisa') # pega o valor pesquisa enviado pela query, que contém a pesquisa que o usuário fez para encontrar aquela música

        return render(request,'cifras/perfilmusica.html',context)
    
#------------ VIEWS PARA MODEL MusicasAprender ------------

# view que cria um objeto "MusicasAprender"
class CreateMusicasAprender(View):
    def post(self,request,*args,**kwargs):
        id_musica = self.request.POST.get('id_musica')
        capa_album_medium = self.request.POST.get('imagem_album_medium')
        capa_album_small = self.request.POST.get('imagem_album_small')
        nome_banda = self.request.POST.get('nome_banda')
        nome_musica = self.request.POST.get('nome_musica')
        duracao = self.request.POST.get('duracao')
        bpm = float(self.request.POST.get('bpm')) # o campo bpm chega como uma string que guarda um número decimal e nós transformamos em float
        bpm = round(bpm) # aqui pegamos esse float e arredondamos para cima, tornando ela um INT(nosso campo "bpm" do model só aceita valores inteiros)
        instrumento = self.request.POST.get('instrumento')

        obj = MusicasAprender.objects.create(user = request.user,capa_album_small = capa_album_small,capa_album_medium = capa_album_medium,nome_banda = nome_banda,nome_musica = nome_musica, duracao = duracao, bpm = bpm, instrumento = instrumento)

        if obj:
            caminho_perfilmusica = reverse('url_perfilmusica',kwargs={'id': id_musica}) # usa a função reverse para pegar o caminho da URL que tem o nome programado igual a 'url_perfilmusica', informando o name da URL e o valor a ser armazenado no Kwargs <int:id>

            # usa a função python(urlencode) para codificar o dicionario para ser usado como querystring, para mandar no redirect os valores que a view PerfilMusica precisa(pagina e pesquisa)
            parametros_url = urlencode({
                'pagina' : self.request.POST.get('pagina'), # pega os parametro da pagina em que o usuário estava enviada no formulário
                'pesquisa': self.request.POST.get('pesquisa') # pega o parametro da pesquisa que o usuário fez 
            })

            return redirect(f"{caminho_perfilmusica}?{parametros_url}") # volta para a pagina de perfil da música, mandando todo os parametros necessário para a view PerfilMusica funcionar perfeitamente
        
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
            return MusicasAprender.objects.filter(user = self.request.user ,instrumento = query) # Se o programa encontrar o filtro no metodo GET do request(informação pela url do site) ele retorna os objetos com instrumento igual à palavra encontrada no GET
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = "MusicasAprender"
        context['objeto'] = self.object_list # object_list salva o retorno do get_queryset, guarda os objetos a serem listados no template. Se estiver vazio o template verifica e exibe uma mensagem
        return context

# para atualizar o campo instrumento do "MusicasAprender"
class UpdateMusicasAprender(FormView):
    template_name = 'cifras/musicasForm.html'
    form_class = MusicaAprenderForm
    success_url = reverse_lazy('url_listmusicasaprender')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['id_musica_aprender'] = self.kwargs['pk'] # pega o id enviado pela URL e armazenado no kwargs da URL(self.kwargs) e armazena no contexto

        return context # envio o contexto para o template
    
    # uso a função que manipula o kwargs do form
    def get_form_kwargs(self):
        id = self.kwargs['pk'] # busco no kwargs o id que a view recebeu pela URL
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = get_object_or_404(MusicasAprender,pk = id) # escrevo no atributo instance do kwargs uma instancia de objeto existente para ja vir com campos preenchidos
        return kwargs
    
    def form_valid(self, form):
        form.save() # salva o formulário(no FormView é preciso salvar manualmente, em UpdateView e CreateView por exemplo, não é necessário)
        return super().form_valid(form) # retorna


# view para detalhes de um objeto "MusicasAprender"
class PerfilMusicaAprender(DetailView):
    model = MusicasAprender
    template_name = 'cifras/perfilmusicasaprender.html'
    context_object_name = "musica"

# View para deletar um objeto específico "MusicasAprender"
class DeleteMusicasAprender(DeleteView):
    model = MusicasAprender
    template_name = 'cifras/deletemusicas.html'
    success_url = reverse_lazy('url_listmusicasaprender')

    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['musica_aprender'] = "model_musica_aprender" # especifica para o template que o model que acessa é o MusicasAprender

        return context

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
            return MusicasAprendidas.objects.filter(musica__user = self.request.user ,musica__instrumento = query) # em Django, usamos duas underlines("__") para acessar campos do objeto referenciado numa ForeignKey, no nosso caso queremos acesso ao campo instrumento do objeto "MusicasAprender" que é referenciado no campo musica do model "MusicasAprendidas" na ForeignKey "musica"
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = "MusicasAprendidas"
        context['objeto'] = self.object_list # object_list salva o retorno do get_queryset, guarda os objetos a serem listados no template. Se estiver vazio o template verifica e exibe uma mensagem
        return context

# class para detalhe de uma música aprendida
class MusicaAprendidaDetail(DetailView):
    model = MusicasAprendidas
    template_name = 'cifras/perfilmusicasaprendidas.html'
    context_object_name = 'musica_aprendida'

# class para excluir uma música aprendida
class MusicaAprendidaDelete(DeleteView):
    model = MusicasAprendidas
    template_name = 'cifras/deletemusicas.html'
    success_url = reverse_lazy('url_listmusicasaprendidas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['musica_aprendida'] = "model_musica_aprendida" # especifica para o template que o model que acessa é o MusicasAprendidas

        return context

class MusicaAprendidaUpdate(FormView):
    template_name = "cifras/musicasForm.html"
    form_class = MusicaAprendidaForm
    success_url = reverse_lazy('url_listmusicasaprendidas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['id_musica_aprendida'] = self.kwargs['pk'] # pega o id enviado pela URL e armazenado no kwargs da URL(self.kwargs) e armazena no contexto

        return context # envio o contexto para o template

    def get_form_kwargs(self):
        id = self.kwargs['pk'] # busco no kwargs o id que a view recebeu pela URL
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = get_object_or_404(MusicasAprendidas,pk = id)  # escrevo no atributo instance do kwargs uma instancia de objeto existente para ja vir com campos preenchidos

        return kwargs

    def form_valid(self, form):
        form.save() # salva o formulário(no FormView é preciso salvar manualmente, em UpdateView por exemplo, não é necessário)
        return super().form_valid(form) 

#------------ View para Perfil do Usuário ------------
class PerfilUser(View):
    def get(self,request,*args,**kwargs):
        if request.GET.get('filtro') == "musicasaprendidas":
            return redirect('url_listmusicasaprendidas')
        elif request.GET.get('filtro') == "musicasaprender":
            return redirect('url_listmusicasaprender')

        return render (request,"cifras/perfil.html")
