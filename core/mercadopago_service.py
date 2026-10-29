import logging
from decimal import Decimal

import mercadopago
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from core.models import Frete

logger = logging.getLogger(__name__)


class PagamentoErro(Exception):
    """Erro de negócio no fluxo de pagamento. A mensagem é segura para mostrar ao usuário."""


# payment_type_id do Mercado Pago -> forma de pagamento do nosso modelo
FORMA_POR_TIPO = {
    'credit_card': Frete.CARTAO,
    'debit_card': Frete.CARTAO,
    'prepaid_card': Frete.CARTAO,
    'ticket': Frete.BOLETO,
    'bank_transfer': Frete.PIX,
    'account_money': Frete.OUTRO,
}


def _sdk():
    token = getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', '')
    print(f'[DEBUG] _sdk chamado, token com {len(token)} caracteres')
    if not token:
        raise PagamentoErro('O pagamento online ainda não foi configurado no servidor.')
    return mercadopago.SDK(token)


def criar_preferencia(frete):
    """Cria o checkout no Mercado Pago e devolve a URL para onde o cliente deve ir."""
    if frete.status_pagamento == Frete.PAGO:
        raise PagamentoErro('Este frete já foi pago.')
    if frete.moeda != Frete.RS:
        raise PagamentoErro('O pagamento online está disponível apenas para fretes em Reais.')
    if frete.valor_frete <= 0:
        raise PagamentoErro('O valor do frete é inválido.')

    front = settings.FRONTEND_URL.rstrip('/')
    retorno = f'{front}/pagamento-retorno'

    dados = {
        'items': [{
            'id': str(frete.id),
            'title': f'Frete #{frete.id}',
            'quantity': 1,
            'currency_id': 'BRL',
            'unit_price': float(frete.valor_frete),
        }],
        'external_reference': str(frete.id),
        'back_urls': {
            'success': retorno,
            'pending': retorno,
            'failure': retorno,
        },
    }

    # Retorno automático só funciona com site em https (em localhost o cliente clica em "Voltar ao site")
    if front.startswith('https://'):
        dados['auto_return'] = 'approved'

    webhook = getattr(settings, 'MERCADOPAGO_WEBHOOK_URL', '')
    if webhook:
        dados['notification_url'] = webhook

    resultado = _sdk().preference().create(dados)
    if resultado.get('status') not in (200, 201):
        logger.error('Erro ao criar preferência no Mercado Pago: %s', resultado)
        raise PagamentoErro('Não foi possível iniciar o pagamento no Mercado Pago.')

    resposta = resultado['response']
    return {
        'checkout_url': resposta['init_point'],
        'preference_id': resposta['id'],
    }


def buscar_pagamento(payment_id):
    """Consulta um pagamento direto na API do Mercado Pago (fonte da verdade)."""
    payment_id = str(payment_id)
    if not payment_id.isdigit():
        raise PagamentoErro('Identificador de pagamento inválido.')

    resultado = _sdk().payment().get(payment_id)
    if resultado.get('status') != 200:
        raise PagamentoErro('Pagamento não encontrado no Mercado Pago.')
    return resultado['response']


def buscar_pagamento_do_frete(frete):
    """Procura o pagamento mais relevante deste frete (prefere o aprovado)."""
    resultado = _sdk().payment().search({
        'external_reference': str(frete.id),
        'sort': 'date_created',
        'criteria': 'desc',
    })
    if resultado.get('status') != 200:
        return None

    pagamentos = resultado['response'].get('results', [])
    for pagamento in pagamentos:
        if pagamento.get('status') == 'approved':
            return pagamento
    return pagamentos[0] if pagamentos else None


def aplicar_pagamento(frete, pagamento):
    """
    Marca o frete como pago SE o pagamento for válido para ele.
    Retorna True se o frete está pago. É seguro chamar várias vezes (idempotente).
    """
    if str(pagamento.get('external_reference')) != str(frete.id):
        raise PagamentoErro('Este pagamento não pertence a este frete.')

    if pagamento.get('status') != 'approved':
        return False

    pago = Decimal(str(pagamento.get('transaction_amount') or 0))
    if pago < frete.valor_frete:
        raise PagamentoErro('O valor pago é menor que o valor do frete.')

    data_pagamento = parse_datetime(pagamento.get('date_approved') or '') or timezone.now()
    forma = FORMA_POR_TIPO.get(pagamento.get('payment_type_id'), Frete.OUTRO)

    # Só atualiza se ainda estiver pendente: evita duplicar caso o webhook e o retorno cheguem juntos
    atualizados = Frete.objects.filter(
        pk=frete.pk, status_pagamento=Frete.PENDENTE
    ).update(
        status_pagamento=Frete.PAGO,
        forma_pagamento=forma,
        data_pagamento=data_pagamento,
        mp_payment_id=str(pagamento['id']),
    )

    if atualizados:
        # Só confirma o frete se ele ainda não avançou no fluxo (ex.: já em rota)
        Frete.objects.filter(pk=frete.pk, status='PENDENTE').update(status='CONFIRMADO')

    frete.refresh_from_db()
    return True