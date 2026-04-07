from rest_framework.viewsets import ModelViewSet
from core.models import Rota
from core.serializers import RotaSerializer

class RotaViewSet(ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer