from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from core.models import Rota, Frete
from core.serializers import RotaSerializer

class RotaViewSet(ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Rota.objects.all()
        return Rota.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    # Nova validação de exclusão
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Frete.objects.filter(rota=instance).exists():
            raise ValidationError({"detail": "Não é permitido excluir rotas vinculadas a fretes."})
        return super().destroy(request, *args, **kwargs)