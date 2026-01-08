# Импорт всего для сигналов.
import os
import shutil
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.http import HttpResponseServerError

import logging
logger = logging.getLogger('project')


