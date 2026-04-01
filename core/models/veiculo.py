from django.db import models

class Veiculo (models.Model):
    placa = models.CharField(max_length=7)
    modelo = models.CharField(max_length=40)
    capcacidade = models.DecimalField(max_digits=5, decimal_places=0)

    def __str__(self):
        return f"{self.id} {self.placa} {self.modelo} {self.capcacidade}"