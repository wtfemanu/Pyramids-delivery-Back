from django.db import models
from .carga import Carga
from .motorista import Motorista
from .veiculo import Veiculo
from .rota import Rota

class Frete(models.Model):

    RS = 'Reais'
    EU ='Euro'
    S = 'Dolar'
    
    UNIDADES_MOEDAS=[
         (RS, 'Reais'),
        (EU, 'Euros'),
        (S, 'Dólares'),
    ]
    
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE, db_column='id_rota')
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

    def __str__(self):
        return f"{self.id} - {self.carga} {self.rota} ({self.valor_frete} {self.status})  {self.motorista} {self.veiculo} {self.rota}"