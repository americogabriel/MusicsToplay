from django import forms
from .models import MusicasAprender,MusicasAprendidas
from django.contrib.auth.models import User

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

# formulário simples para login com campos de username e login
class LoginUserForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="senha")

class CadastroUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password"]


    def save(self, commit = True):
        user = super().save(commit = False) # chamo o método save da classe pai mas com o atributo commit = False para retornar a instância do formulário sem salvar a instância no banco de dados
        user.set_password(self.cleaned_data["password"]) # uso o set_password para transformar a senha num hash criptografado, cleaned_data["campo_form"] é usado para pegar o valor enviado no campo do form
        if commit:
            user.save()

        return user
            