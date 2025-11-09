# from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class PackageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'package'
    verbose_name = ('package')
