# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Pub, Item, Bill, Order

admin.site.register(Pub)
admin.site.register(Bill)
admin.site.register(Item)
admin.site.register(Order)
