#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.auth.models import User

@shared_task
def send_validation_email(userID, subject, body):
  user = User.objects.get(pk=userID)
  print ("posilam email pro user: ", user)
  user.email_user(subject, body)
