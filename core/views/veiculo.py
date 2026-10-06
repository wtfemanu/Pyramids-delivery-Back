from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from core.models import Veiculo, Frete
from core.serializers import VeiculoSerializer

class VeiculoViewSet(ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Veiculo.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        fretes_ativos = Frete.objects.filter(veiculo=instance).exclude(status__iexact='concluido').exclude(status__iexact='entregue')
        if fretes_ativos.exists():
            raise ValidationError({"detail": "Não é permitido excluir veículos vinculados a fretes ativos."})
        return super().destroy(request, *args, **kwargs)