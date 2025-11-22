from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccessControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accessrequestsapi.access_control'
    verbose_name = _("Access Control")
