from rest_framework.serializers import ModelSerializer
from core.models import Motorista

class MotoristaSerializer(ModelSerializer):
    class Meta:
        model = Motorista
        fields = '__all__'