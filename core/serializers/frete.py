from rest_framework.serializers import ModelSerializer
from core.models import Frete

class FreteSerializer(ModelSerializer):
    class Meta:
        model = Frete
        fields = '__all__'