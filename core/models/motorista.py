from django.db import models

class Motorista (models.Model):
    nome = models.CharField(max_length=120)
    cnh = models.CharField(max_length=11 )

    def __str__(self):
        return f"{self.id} {self.nome} {self.cnh}"