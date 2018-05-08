import json
import logging
from datetime import datetime

from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from pretix.base.payment import BasePaymentProvider, PaymentException
from pretix.base.services.orders import mark_order_paid

logger = logging.getLogger('pretix.plugins.payment_cash')


class Cash(BasePaymentProvider):
    identifier = 'cash'
    verbose_name = _('Cash')

    def is_allowed(self, request):
        user = request.user

        if not user.is_authenticated():
            return False

        return super().is_allowed(request)

    def payment_is_valid_session(self, request):
        return True

    def payment_form_render(self, request) -> str:
        template = get_template('pretix_payment_cash/payment_form.html')
        ctx = {
            'request': request,
            'event': self.event,
            'settings': self.settings,
            'info': request.GET
        }
        return template.render(ctx)

    def checkout_confirm_render(self, request) -> str:
        template = get_template('pretix_payment_cash/checkout_confirm.html')
        ctx = {
            'request': request,
            'event': self.event,
            'settings': self.settings
        }
        return template.render(ctx)

    def payment_perform(self, request, order) -> str:
        info = {
            'payment_date': datetime.now().strftime('%Y%m%dT%H%M%S')
        }

        try:
            mark_order_paid(order, Cash.identifier, send_mail=False, info=json.dumps(info), user=request.user)
        except Exception as e:
            raise PaymentException(_('Cash payment error: {}').format(e))

        return None

    def order_pending_render(self, request, order):
        template = get_template('pretix_payment_cash/order_pending.html')
        ctx = {
            'request': request,
            'order': order,
            'event': self.event,
            'info': self.get_payment_info(order)
        }
        return template.render(ctx)

    def order_paid_render(self, request, order) -> str:
        template = get_template('pretix_payment_cash/order_paid.html')
        ctx = {
            'request': request,
            'order': order,
            'event': self.event,
            'info': self.get_payment_info(order)
        }
        return template.render(ctx)

    def get_payment_info(self, order):
        return json.loads(order.payment_info) if order.payment_info is not None else {}
