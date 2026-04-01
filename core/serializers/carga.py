from rest_framework.serializers import ModelSerializer
from core.models import Carga

class CargaSerializer(ModelSerializer):
    class Meta:
        model = Carga
        fields = '__all__'