from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Frete
from core.serializers import FreteSerializer
class FreteViewSet(viewsets.ModelViewSet):
    queryset = Frete.objects.all()
    serializer_class = FreteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        # Usuários comuns só listam seus próprios fretes
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Frete.objects.all()
        return Frete.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # MÁGICA AQUI: Salva o frete associando automaticamente ao usuário logado
        serializer.save(usuario=self.request.user)