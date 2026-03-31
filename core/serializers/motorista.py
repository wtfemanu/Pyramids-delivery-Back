from rest_framework.serializers import ModelSerializer
from core.models import Motorista
from attr import fields


class MotoristaSerializer(ModelSerializer):
    class Meta:
        model = Motorista
        fields = '__all__'