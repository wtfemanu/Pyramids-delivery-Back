from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Frete, Motorista
from core.serializers.frete import FreteSerializer
from core.mercadopago_service import (
    PagamentoErro,
    criar_preferencia,
    buscar_pagamento,
    buscar_pagamento_do_frete,
    aplicar_pagamento,
)


class FreteViewSet(viewsets.ModelViewSet):
    queryset = Frete.objects.all()
    serializer_class = FreteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        tipo = self.request.query_params.get('tipo', None)
        data_filtro = self.request.query_params.get('data', None)

        # Administrador vê TODOS os fretes (exceto se requisitar especificamente os seus como motorista)
        if user.is_superuser or user.is_staff:
            if tipo == 'motorista':
                motorista_obj = Motorista.objects.filter(user=user).first()
                if motorista_obj:
                    queryset = Frete.objects.filter(motorista=motorista_obj)
                else:
                    queryset = Frete.objects.none()
            else:
                queryset = Frete.objects.all()
        else:
            # Utilizador comum: vê apenas os seus próprios fretes (ou como motorista se aplicável)
            if tipo == 'motorista':
                motorista_obj = Motorista.objects.filter(user=user).first()
                if motorista_obj:
                    queryset = Frete.objects.filter(motorista=motorista_obj)
                else:
                    queryset = Frete.objects.none()
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

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        """Cria o checkout no Mercado Pago e devolve a URL de pagamento."""
        frete = self.get_object()
        try:
            dados = criar_preferencia(frete)
        except PagamentoErro as erro:
            return Response({'detail': str(erro)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(dados, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='confirmar-pagamento')
    def confirmar_pagamento(self, request, pk=None):
        """
        Confere no Mercado Pago se o frete foi pago e atualiza o banco.
        Recebe `payment_id` (opcional). Sem ele, procura o pagamento pelo frete.
        """
        frete = self.get_object()
        status_mp = None

        if frete.status_pagamento != Frete.PAGO:
            payment_id = request.data.get('payment_id')
            try:
                if payment_id:
                    pagamento = buscar_pagamento(payment_id)
                else:
                    pagamento = buscar_pagamento_do_frete(frete)

                if pagamento:
                    status_mp = pagamento.get('status')
                    aplicar_pagamento(frete, pagamento)
            except PagamentoErro as erro:
                return Response({'detail': str(erro)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'pago': frete.status_pagamento == Frete.PAGO,
            'status_mp': status_mp,
            'frete': self.get_serializer(frete).data,
        })