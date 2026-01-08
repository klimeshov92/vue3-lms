
from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.http import HttpResponseServerError
from .models import *
from datetime import datetime, timedelta
from django.db import transaction

import logging
logger = logging.getLogger('project')


