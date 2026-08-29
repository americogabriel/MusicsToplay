from django.shortcuts import render
from django.urls import reverse_lazy
from .models import MusicasAprender
from django.views.generic import CreateView,ListView,UpdateView,DeleteView

def Home(request):
    return render(request,template_name='cifras/home.html')

class CreateMusicasAprender(CreateView):
    model = MusicasAprender
    fields = ['nome_banda','nome_musica','duracao','tom_musica','instrumento']
    template_name = 'cifras/createMusicasAprender.html'
    success_url = reverse_lazy('url_home')


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


class UpdateMusicasAprender(UpdateView):
    model = MusicasAprender
    fields = ['nome_banda','nome_musica','duracao','tom_musica','instrumento']
    template_name = 'cifras/updateMusicas.html'
    success_url = reverse_lazy('url_listmusicas')


class DeleteMusicasAprender(DeleteView):
    model = MusicasAprender
    template_name = 'cifras/deletemusicas.html'
    success_url = reverse_lazy('url_listmusicas')
