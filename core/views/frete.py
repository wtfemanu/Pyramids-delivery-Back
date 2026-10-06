from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from core.models import Frete, Motorista
from core.serializers.frete import FreteSerializer

class FreteViewSet(viewsets.ModelViewSet):
    queryset = Frete.objects.all()
    serializer_class = FreteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        tipo = self.request.query_params.get('tipo', None)
        data_filtro = self.request.query_params.get('data', None)

        # Se for superuser/staff e NÃO especificou tipo, vê tudo
        if (user.is_superuser or user.is_staff) and not tipo:
            queryset = Frete.objects.all()
        elif tipo == 'motorista':
            # Localiza o motorista logado através da relação 'user'
            motorista_obj = Motorista.objects.filter(user=user).first()
            if motorista_obj:
                queryset = Frete.objects.filter(motorista=motorista_obj)
            else:
                queryset = Frete.objects.none()
        else:
            # Utilizador comum: VÊ APENAS OS SEUS PRÓPRIOS FRETES
            if user.is_superuser or user.is_staff:
                fretes_proprios = Frete.objects.filter(usuario=user)
                queryset = fretes_proprios if fretes_proprios.exists() else Frete.objects.all()
            else:
                queryset = Frete.objects.filter(usuario=user)

        if data_filtro:
            queryset = queryset.filter(data_criacao__date=data_filtro)

        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        
        if self.action in ['retrieve', 'update', 'partial_update']:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            
            user = self.request.user
            if user.is_superuser or user.is_staff:
                obj = Frete.objects.filter(**filter_kwargs).first()
            else:
                motorista_obj = Motorista.objects.filter(user=user).first()
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