from rest_framework import viewsets  # <--- Mudança aqui
from rest_framework.permissions import IsAuthenticated
from core.models import Carga
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