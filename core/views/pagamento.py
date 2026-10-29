import logging

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Frete
from core.mercadopago_service import PagamentoErro, buscar_pagamento, aplicar_pagamento

logger = logging.getLogger(__name__)


class MercadoPagoWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        corpo = request.data if isinstance(request.data, dict) else {}
        dados = corpo.get('data') if isinstance(corpo.get('data'), dict) else {}

        tipo = corpo.get('type') or request.query_params.get('type') or request.query_params.get('topic')
        payment_id = dados.get('id') or request.query_params.get('data.id') or request.query_params.get('id')

        if tipo == 'payment' and payment_id:
            try:
                pagamento = buscar_pagamento(payment_id)
                frete = Frete.objects.filter(pk=pagamento.get('external_reference')).first()
                if frete:
                    aplicar_pagamento(frete, pagamento)
            except (PagamentoErro, ValueError) as erro:
                logger.warning('Webhook Mercado Pago ignorado: %s', erro)

        # Sempre 200, senão o Mercado Pago fica reenviando a notificação
        return Response(status=200)