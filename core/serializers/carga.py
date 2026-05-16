from rest_framework import serializers
from core.models import Carga

class CargaSerializer(serializers.ModelSerializer):
    # Gera a URL completa da imagem para o frontend Vue consumir sem problemas
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Carga
        fields = '__all__'

    def get_foto_url(self, obj):
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None