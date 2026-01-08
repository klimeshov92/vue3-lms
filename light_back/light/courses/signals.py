# Импорт всего для сигналов.
import os
import shutil
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.http import HttpResponseServerError
from .models import Course

import logging
logger = logging.getLogger('project')

@receiver(post_delete, sender=Course)
def delete_scorm_package_directory(sender, instance, **kwargs):
    try:
        directory_path = os.path.join(settings.MEDIA_ROOT, 'scorm_packages', str(instance.id))

        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            logger.info(f"Успешное удаление директории SCORM-пакета {instance.id} по пути {directory_path}")
        else:
            logger.warning(f"Директория SCORM-пакета {instance.id} по пути {directory_path} не существует")

    except Exception as e:
        logger.error(f"Ошибка при удалении директории SCORM-пакета {instance.id}: {str(e)}")
        if settings.DEBUG:
            raise
