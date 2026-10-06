from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from core.models import Motorista, Frete
from core.serializers import MotoristaSerializer

class MotoristaViewSet(ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Motorista.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        fretes_ativos = Frete.objects.filter(motorista=instance).exclude(status__iexact='concluido').exclude(status__iexact='entregue')
        if fretes_ativos.exists():
            raise ValidationError({"detail": "Não é permitido excluir motoristas vinculados a fretes ativos."})
        return super().destroy(request, *args, **kwargs)