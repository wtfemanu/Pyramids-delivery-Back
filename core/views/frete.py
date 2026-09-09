from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from core.models import Frete, Motorista
from core.serializers import FreteSerializer

class FreteViewSet(viewsets.ModelViewSet):
    queryset = Frete.objects.all()
    serializer_class = FreteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        tipo = self.request.query_params.get('tipo', None)

        # 👑 1. Superuser / Staff sem parâmetro de tipo (Visão Administrativa Total)
        if (user.is_superuser or user.is_staff) and not tipo:
            return Frete.objects.all()

        # 🚚 2. ABA / PAINEL DO MOTORISTA (?tipo=motorista)
        if tipo == 'motorista':
            # Como a model Motorista utiliza 'user', buscamos por ela
            motorista_obj = Motorista.objects.filter(user=user).first()
            if not motorista_obj and hasattr(Motorista, 'usuario'):
                motorista_obj = Motorista.objects.filter(usuario=user).first()

            # Se for admin testando a visão de motorista
            if user.is_superuser or user.is_staff:
                if motorista_obj:
                    return Frete.objects.filter(motorista=motorista_obj)
                return Frete.objects.all()

            # Motorista comum: apenas as entregas atribuídas a ele
            if motorista_obj:
                return Frete.objects.filter(motorista=motorista_obj)
            
            return Frete.objects.none()

        # 📦 3. ABA / PAINEL DO CLIENTE (?tipo=cliente ou padrão)
        if user.is_superuser or user.is_staff:
            fretes_proprios = Frete.objects.filter(usuario=user)
            return fretes_proprios if fretes_proprios.exists() else Frete.objects.all()

        return Frete.objects.filter(usuario=user)

    def get_object(self):
        """
        Garante que operações individuais (PATCH, PUT, GET de ID específico) 
        encontrem o frete tanto se o usuário for o criador quanto se for o motorista atribuído.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        if self.action in ['retrieve', 'update', 'partial_update']:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            
            user = self.request.user
            if user.is_superuser or user.is_staff:
                obj = Frete.objects.filter(**filter_kwargs).first()
            else:
                motorista_obj = Motorista.objects.filter(user=user).first()
                if not motorista_obj and hasattr(Motorista, 'usuario'):
                    motorista_obj = Motorista.objects.filter(usuario=user).first()
                
                if motorista_obj:
                    obj = Frete.objects.filter(
                        Q(id=filter_kwargs['pk']) & (Q(usuario=user) | Q(motorista=motorista_obj))
                    ).first()
                else:
                    obj = Frete.objects.filter(id=filter_kwargs['pk'], usuario=user).first()
            
            if obj:
                self.check_object_permissions(self.request, obj)
                return obj

        return super().get_object()

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)