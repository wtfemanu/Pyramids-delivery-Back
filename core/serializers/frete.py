from rest_framework import serializers
from core.models import Frete
from django.apps import apps 

class FreteSerializer(serializers.ModelSerializer):
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = Frete
        fields = '__all__'
        read_only_fields = ('usuario', 'data_criacao')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = self.context.get('request')
        if request and request.user and not (request.user.is_superuser or request.user.is_staff):
            CargaModel = apps.get_model('core', 'Carga')
            self.fields['carga'].queryset = CargaModel.objects.filter(usuario=request.user)

    def validate(self, data):
        # Força o status inicial como PENDENTE se não vier preenchido
        if not data.get('status'):
            data['status'] = 'PENDENTE'

        motorista = data.get('motorista')
        if motorista:
            frete_ativo_existente = Frete.objects.filter(
                motorista=motorista, 
                status__in=['PENDENTE', 'EM_TRANSITO']
            )
            if self.instance:
                frete_ativo_existente = frete_ativo_existente.exclude(pk=self.instance.pk)
            
            if frete_ativo_existente.exists():
                raise serializers.ValidationError(
                    {"motorista": "Este motorista já possui um frete ativo no momento e não está disponível."}
                )
        return data