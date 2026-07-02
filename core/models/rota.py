from django.conf import settings
from django.db import models

class Rota(models.Model):
    # Relaciona a rota com o usuário que a criou
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="rotas"
    )
    ponto_inicial = models.CharField(max_length=150)
    ponto_final = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.id} {self.ponto_inicial} -> {self.ponto_final}"