#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Manager, Model, CharField, PositiveSmallIntegerField, ForeignKey, \
CASCADE, Sum, F, SET_NULL, BooleanField
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.urls import reverse

class BaseInfo(Model):
  class Meta:
    abstract = True

  owner = ForeignKey(User, on_delete = SET_NULL, null = True, blank = True)
  name = CharField(max_length=51, unique=True, verbose_name="Název")
  isBase = BooleanField(default=False)

  def isOwner(self, user):
    return user == self.owner or user.is_staff

  def __unicode__(self):
    return '%s' % self.name

  def clean(self):
    self.name = self.name.capitalize()

class Item(BaseInfo):
  class Meta:
    verbose_name = "Položka"
    default_related_name = "items"
    unique_together = ("name", "pub")

  ITEM_CATEGORY = (
      ('N', 'Nápoje'),
      ('J', 'Jídlo'),
      ('O', 'Ostatní'),
      )

  price = PositiveSmallIntegerField(default=1, verbose_name="Cena")
  category = CharField(max_length=1, choices=ITEM_CATEGORY, default='N', verbose_name="Kategorie")
  pub = ForeignKey('Pub', on_delete=CASCADE, verbose_name="Hospoda")

  def get_absolute_url(self):
    return reverse('beercounter:pub', kwargs={'pk': self.pub_id})

class Bill(BaseInfo):
  class Meta:
    unique_together = ('name', 'pub')
    default_related_name = "bills"
    verbose_name = "Účet"

  pub = ForeignKey('Pub', on_delete=CASCADE, )

  @property
  def spending(self):
    # vrací celkový součet účtu
    return self.orders.aggregate(spending=Sum(F('count')*F('item__price')))['spending']

  def get_absolute_url(self):
    return reverse('beercounter:pub', kwargs={'pk': self.pub.pk})

class Pub(BaseInfo):
  class Meta:
    verbose_name = "Hospoda"
    unique_together = ('name', 'owner')
    ordering = ('name', )


  def get_absolute_url(self):
    return reverse('beercounter:index')

class Order(Model):
  class Meta:
    unique_together = ('bill','item')
    default_related_name="orders"
    verbose_name = "Objednávka"

  bill = ForeignKey('Bill', on_delete=CASCADE, verbose_name="Účet")
  item = ForeignKey('Item', on_delete=CASCADE, verbose_name="Položka")
  count = PositiveSmallIntegerField(default=1, verbose_name="Počet")

  @property
  def total_cost(self):
    return self.item.price * self.count

  def __unicode__(self):
    return '%s' % self.item.name

  def get_absolute_url(self):
    return reverse('beercounter:bill', kwargs={'pk': self.bill.pk})
