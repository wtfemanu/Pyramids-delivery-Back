from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError  # <-- Adicionado
from core.models import Carga, Frete                  # <-- Adicionado Frete
from core.serializers import CargaSerializer

class CargaViewSet(viewsets.ModelViewSet):
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Carga.objects.all()
        return Carga.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    # Nova validação de exclusão
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Verifica se esta carga está vinculada a qualquer frete
        if Frete.objects.filter(carga=instance).exists():
            raise ValidationError({"detail": "Não é permitido excluir cargas vinculadas a fretes."})
        return super().destroy(request, *args, **kwargs)