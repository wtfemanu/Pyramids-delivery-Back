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
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Motorista.objects.all()
        return Motorista.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    # Nova validação de exclusão (Apenas fretes ativos/não concluídos barram, conforme RN013.1)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Filtra por fretes deste motorista cujo status NÃO seja 'Concluído' (ou 'Entregue')
        fretes_ativos = Frete.objects.filter(motorista=instance).exclude(status__iexact='concluido').exclude(status__iexact='entregue')
        if fretes_ativos.exists():
            raise ValidationError({"detail": "Não é permitido excluir motoristas vinculados a fretes ativos."})
        return super().destroy(request, *args, **kwargs)