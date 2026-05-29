from rest_framework import serializers
from core.models import Carga

class CargaSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Carga
        fields = '__all__'
        read_only_fields = ('usuario',) # <--- ADICIONE ESTA LINHA

    def get_foto_url(self, obj):
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None