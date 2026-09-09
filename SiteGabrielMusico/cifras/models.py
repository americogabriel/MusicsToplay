from django.db import models

class MusicasAprender(models.Model):

    # tupla de escolhas(o primeiro valor é o valor armazenado no campo e o segundo é o valor que aparece para usuário quando consultado pelo próprio)
    INSTRUMENTO_CHOICES = (
        ('Guitarra','Guitarra'),
        ('Violao','Violão'),
    )
    capa_album = models.ImageField()
    nome_banda = models.CharField(max_length=40)
    nome_musica = models.CharField(max_length=40)
    duracao = models.IntegerField()
    bpm = models.IntegerField()
    instrumento = models.CharField(choices= INSTRUMENTO_CHOICES,default= 'violao') # com o conjunto de tuplas(INSTRUMENTO_CHOICES), usamos o atributo choice para o campo ter somente as opções da tupla como valor e o default dita um valor que caso o campo fique em branco este valor padrão será o valor do campo.

    ## classe Meta
    class Meta:
        verbose_name_plural = "MusicasAprender" # o atributo verbose_name_plural controla como o nome vai ficar no plural quando for pro painel django admin

    ## def __str__ é um método que retorna o titulo de cada objeto no painel do django admin, podemos modificar esse titulo colocando o valor de qualquer atributo do model(neste caso foi o atributo nome_musica)
    def __str__(self):
        
        return self.nome_musica

class MusicasAprendidas(models.Model):

    # tupla de escolhas
    DIFICULTADE_CHOICES = (
        (0,0),
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )

    musica = models.ForeignKey(MusicasAprender,on_delete=models.SET_NULL, null = True) # models.SET_NULL permite o objeto referenciado ser apagado, quando apagado, objeto que o referencia tera o campo musica substituido por NULL
    dominio = models.IntegerField(choices=DIFICULTADE_CHOICES) # usa a tupla de escolhas para limitar os valoes a somente os que estão na tupla, que nem o campo instrumento da classe MusicaAprender

    # classe Meta
    class Meta:
        verbose_name_plural = "MusicasAprendidas" # o atributo verbose_name_plural controla como o nome vai ficar no plural quando for pro painel django admin

    
    def __str__(self):
        if self.musica is None:
            return "Referencia Apagada" # se musica for None quer dizer que o objeto referenciado no campo ForeignKey foi apagado
        return self.musica.nome_musica
    
