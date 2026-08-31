from django.urls import path
from .views import Home,CreateMusicasAprender,ListMusicasAprender,UpdateMusicasAprender,DeleteMusicasAprender,PerfilMusica

urlpatterns = [
    path('',Home.as_view(), name = 'url_home'),
    path('createmusica/',CreateMusicasAprender.as_view(),name= 'url_createmusica'),
    path('listmusicas/',ListMusicasAprender.as_view(), name = 'url_listmusicas'),
    path('updatemusicas/<int:pk>',UpdateMusicasAprender.as_view(), name = 'url_updatemusicas'),
    path('deletemusica/<int:pk>',DeleteMusicasAprender.as_view(), name = 'url_deletemusicas'),
    path('perfilmusica/<int:id>',PerfilMusica.as_view(), name= 'url_perfilmusica')
]