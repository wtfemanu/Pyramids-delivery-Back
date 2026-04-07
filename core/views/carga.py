from rest_framework.viewsets import ModelViewSet
from core.models import Carga
from core.serializers import CargaSerializer

class CargaViewSet(ModelViewSet):
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer