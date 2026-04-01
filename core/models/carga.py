from django.db import models

class Carga(models.Model):
    KG = 'KG'
    TON = 'TON'
    G = 'G'
    
    UNIDADES_PESO_CHOICES = [
        (KG, 'Quilogramas'),
        (TON, 'Toneladas'),
        (G, 'Gramas'),
    ]

    RS = 'Reais'
    EU ='Euro'
    S = 'Dolar'
    
    UNIDADES_MOEDAS=[
         (KG, 'Quilogramas'),
        (TON, 'Toneladas'),
        (G, 'Gramas'),
    ]



    descricao = models.CharField(max_length=255)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(
        max_length=3, 
        choices=UNIDADES_PESO_CHOICES, 
        default=KG
    ) 
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    moeda = models.CharField(
        max_length=3, 
        choices=UNIDADES_MOEDAS, 
        default=RS
    ) 

    def __str__(self):
        return f"{self.id} - {self.descricao} ({self.peso} {self.unidade}) {self.valor} {self.moeda}"