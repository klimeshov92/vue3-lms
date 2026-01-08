
from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.http import HttpResponseServerError
from .models import *
from datetime import datetime, timedelta
from django.db import transaction

import logging
logger = logging.getLogger('project')

@receiver(post_delete, sender=EventTemplate)
def event_group_delete(sender, instance, **kwargs):
    try:

        logger.debug(f"Начало работы сигнала event_group_delete")

        if instance.admin_group:
            instance.admin_group.delete()

        logger.debug(f"Связанные с задачей группы удалены")

    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала event_group_delete: {e}", exc_info=True)
        if settings.DEBUG:
            raise

