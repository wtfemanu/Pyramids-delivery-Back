from rest_framework.viewsets import ModelViewSet
from core.models import Frete
from core.serializers import FreteSerializer

class FreteViewSet(ModelViewSet):
    queryset = Frete.objects.all()
    serializer_class = FreteSerializer
