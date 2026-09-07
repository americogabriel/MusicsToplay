from django.urls import path
from .views import Home,CreateMusicasAprender,ListMusicasAprender,UpdateMusicasAprender,DeleteMusicasAprender,PerfilMusica,PerfilMusicaAprender,CreateMusicasAprendidas,ListMusicasAprendidas,PerfilUser

urlpatterns = [
    # PATH DA Home
    path('',Home.as_view(), name = 'url_home'),
    # URL'S DO MODEL MusicasAprendidas
    path('createmusica/',CreateMusicasAprender.as_view(),name = 'url_createmusica'),
    path('listmusicasaprender/',ListMusicasAprender.as_view(), name = 'url_listmusicasaprender'),
    path('updatemusicas/<int:pk>',UpdateMusicasAprender.as_view(), name = 'url_updatemusicas'),
    path('deletemusica/<int:pk>',DeleteMusicasAprender.as_view(), name = 'url_deletemusicas'),
    path('perfilmusicasaprender/<int:pk>',PerfilMusicaAprender.as_view(), name ='url_perfilmusicaaprender'),# perfil de um objeto do model MusicasAprender
    # PATH para detalhes de uma música no dicionario da API deezer
    path('perfilmusica/<int:id>',PerfilMusica.as_view(), name = 'url_perfilmusica'), # perfil de uma música específica da API do deezer
    # URL'S DO MODEL MusicasAprendidas
    path('createmusicaaprendida/',CreateMusicasAprendidas.as_view(), name = 'url_createmusicasaprendidas'), # URL que recebe dados para criar um objeto do model MusicasAprendidas
    path('listmusicasaprendidas/',ListMusicasAprendidas.as_view(), name = 'url_listmusicasaprendidas'), # URL para ListView, que lista todas as músicas aprendidas presentes no model MusicasAprendidas
    path('perfiluser/',PerfilUser.as_view(), name = 'url_perfiluser')
]