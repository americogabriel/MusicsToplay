from django.urls import path
from .views import Home,CreateMusicasAprender,ListMusicasAprender,UpdateMusicasAprender,DeleteMusicasAprender,PerfilMusica,PerfilMusicaAprender,CreateMusicasAprendidas,ListMusicasAprendidas,PerfilUser,MusicaAprendidaDetail,MusicaAprendidaDelete,MusicaAprendidaUpdate,Login,Cadastro

urlpatterns = [
    # PATH DA Home
    path('cadastro/',Cadastro.as_view(), name = 'url_cadastro'),
    path('',Login.as_view(), name = 'url_login'),
    path('home/',Home.as_view(), name = 'url_home'),

    # URL'S DO MODEL MusicasAprendidas
    path('createmusica/',CreateMusicasAprender.as_view(),name = 'url_createmusicaaprender'),
    path('listmusicasaprender/',ListMusicasAprender.as_view(), name = 'url_listmusicasaprender'),
    path('updatemusicas/<int:pk>',UpdateMusicasAprender.as_view(), name = 'url_updatemusicas'),
    path('deletemusica/<int:pk>',DeleteMusicasAprender.as_view(), name = 'url_deletemusicas'),
    path('perfilmusicasaprender/<int:pk>',PerfilMusicaAprender.as_view(), name ='url_perfilmusicaaprender'),# perfil de um objeto do model MusicasAprender

    # PATH para detalhes de uma música no dicionario da API deezer
    path('perfilmusica/<int:id>',PerfilMusica.as_view(), name = 'url_perfilmusica'), # perfil de uma música específica da API do deezer

    # URL'S DO MODEL MusicasAprendidas
    path('createmusicaaprendida/',CreateMusicasAprendidas.as_view(), name = 'url_createmusicasaprendidas'),
    path('listmusicasaprendidas/',ListMusicasAprendidas.as_view(), name = 'url_listmusicasaprendidas'), 
    path('perfilmusicasaprendidas/<int:pk>',MusicaAprendidaDetail.as_view(), name = 'url_perfilmusicaaprendida'),
    path('deletemusicaaprendida/<int:pk>',MusicaAprendidaDelete.as_view(), name = 'url_musicaaprendidadelete'),
    path('updatemusicasaprendidas/<int:pk>',MusicaAprendidaUpdate.as_view(), name = 'url_updatemusicasaprendidas'),

    # PERFIL USER
    path('perfiluser/',PerfilUser.as_view(), name = 'url_perfiluser')
]