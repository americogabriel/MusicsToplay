from django.urls import path
from .views import Home,CreateMusicasAprender,ListMusicasAprender,UpdateMusicasAprender,DeleteMusicasAprender

urlpatterns = [
    path('',Home, name = 'url_home'),
    path('formcreatemusica/',CreateMusicasAprender.as_view(),name= 'url_createmusica'),
    path('listmusicas/',ListMusicasAprender.as_view(), name = 'url_listmusicas'),
    path('updatemusicas/<int:pk>',UpdateMusicasAprender.as_view(), name = 'url_updatemusicas'),
    path('deletemusica/<int:pk>',DeleteMusicasAprender.as_view(), name = 'url_deletemusicas')
]