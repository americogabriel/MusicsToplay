from django import forms
from .models import MusicasAprender,MusicasAprendidas


# ModelForm do Model MusicasAprender: é usado na view de update 
class MusicaAprenderForm(forms.ModelForm):
    class Meta:
        model = MusicasAprender # model que recebe a alteração
        fields = ["instrumento"] # unico campo que pode receber alterações após ser criado

# ModelForm do Model MusicasAprendidas: é usado na view de update 
class MusicaAprendidaForm(forms.ModelForm):
    class Meta:
        model = MusicasAprendidas # model que recebe a alteração
        fields = ["dominio"] # unico campo que pode receber alterações após ser criado
