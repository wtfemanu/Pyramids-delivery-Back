from rest_framework import serializers
from core.models import Frete
from django.apps import apps 

class RotaSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('core', 'Rota')
        fields = ['id', 'ponto_inicial', 'ponto_final']

class FreteSerializer(serializers.ModelSerializer):
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    # Traz os detalhes completos da rota de forma aninhada e segura para leitura
    rota_detalhes = RotaSimplesSerializer(source='rota', read_only=True)

    class Meta:
        model = Frete
        fields = '__all__'
        read_only_fields = (
            'usuario',
            'data_criacao',
            'status_pagamento',
            'forma_pagamento',
            'data_pagamento',
            'mp_payment_id',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user and not (request.user.is_superuser or request.user.is_staff):
            CargaModel = apps.get_model('core', 'Carga')
            self.fields['carga'].queryset = CargaModel.objects.filter(usuario=request.user)

    def validate(self, data):

        if not data.get('status'):
            data['status'] = 'PENDENTE'

        return data