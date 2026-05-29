from rest_framework import serializers
from core.models import Frete
from django.apps import apps 

class FreteSerializer(serializers.ModelSerializer):
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = Frete
        fields = '__all__'
        read_only_fields = ('usuario',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = self.context.get('request')
        if request and request.user and not (request.user.is_superuser or request.user.is_staff):
            # Busca dinâmica que evita o nó do import
            CargaModel = apps.get_model('core', 'Carga')
            self.fields['carga'].queryset = CargaModel.objects.filter(usuario=request.user)