from django.db import models
from django.conf import settings

class Motorista (models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='motorista_profile',
        null=True, 
        blank=True
    )
    nome = models.CharField(max_length=120)
    cnh = models.CharField(max_length=11, unique= True)
    telefone = models.CharField (max_length=11, unique=False, blank= True, null= True)

    def __str__(self):
        return f"{self.id} {self.nome} {self.cnh}"