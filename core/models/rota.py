from django.db import models

class Rota(models.Model):
    ponto_inicial = models.CharField(max_length=150)
    ponto_final = models.CharField(max_length=150)
    distancia = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id} {self.ponto_inicial} -> {self.ponto_final}"