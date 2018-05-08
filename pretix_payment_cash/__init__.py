from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'pretix_payment_cash'
    verbose_name = 'Cash payment'

    class PretixPluginMeta:
        name = ugettext_lazy('Cash payment')
        author = 'Mikkel Ricky'
        description = ugettext_lazy('Cash payment for Pretix')
        visible = True
        version = '1.0.0'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_payment_cash.PluginApp'
