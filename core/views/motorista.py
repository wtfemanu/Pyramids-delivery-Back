from rest_framework.viewsets import ModelViewSet
from core.models import Motorista
from core.serializers import MotoristaSerializer

class MotoristaViewSet(ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    