from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Account)
admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(Subdivision)
admin.site.register(Position)
admin.site.register(Placement)
admin.site.unregister(Group)
admin.site.register(AccountsGroup)
admin.site.register(ContentType)
admin.site.register(Permission)
admin.site.register(GroupGenerator)
admin.site.register(AccountsGroupObjectPermission)
admin.site.register(AccountObjectPermission)
admin.site.register(HomePage)
admin.site.register(LegalPage)
admin.site.register(PolicyPage)