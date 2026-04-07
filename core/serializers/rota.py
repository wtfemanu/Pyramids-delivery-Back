from rest_framework.serializers import ModelSerializer
from core.models import Rota

class RotaSerializer(ModelSerializer):
    class Meta:
        model = Rota
        fields = '__all__'