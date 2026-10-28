from django.db import models
from django.conf import settings
from .carga import Carga
from .motorista import Motorista
from .veiculo import Veiculo
from .rota import Rota


class Frete(models.Model):

    RS = 'Reais'
    EU = 'Euro'
    S = 'Dolar'

    UNIDADES_MOEDAS = [
        (RS, 'Reais'),
        (EU, 'Euros'),
        (S, 'Dólares'),
    ]

    PENDENTE = 'PENDENTE'
    PAGO = 'PAGO'

    STATUS_PAGAMENTO_CHOICES = [
        (PENDENTE, 'Pendente'),
        (PAGO, 'Pago'),
    ]

    PIX = 'PIX'
    CARTAO = 'CARTAO'
    BOLETO = 'BOLETO'
    OUTRO = 'OUTRO'

    FORMAS_PAGAMENTO_CHOICES = [
        (PIX, 'PIX'),
        (CARTAO, 'Cartão'),
        (BOLETO, 'Boleto'),
        (OUTRO, 'Outro (ex.: saldo Mercado Pago)'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='fretes'
    )
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2)
    moeda = models.CharField(
        max_length=5,
        choices=UNIDADES_MOEDAS,
        default=RS
    )

    status = models.CharField(max_length=50)
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE, db_column='id_carga')
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, db_column='id_motorista')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, db_column='id_veiculo')
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE, db_column='id_rota')
    ultima_localizacao = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Controle de pagamento
    status_pagamento = models.CharField(
        max_length=10,
        choices=STATUS_PAGAMENTO_CHOICES,
        default=PENDENTE
    )
    forma_pagamento = models.CharField(
        max_length=10,
        choices=FORMAS_PAGAMENTO_CHOICES,
        blank=True,
        null=True
    )
    data_pagamento = models.DateTimeField(blank=True, null=True)
    mp_payment_id = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.carga} {self.rota} ({self.valor_frete} {self.status}) {self.motorista} {self.veiculo} {self.rota}"