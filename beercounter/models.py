#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Model, CharField, PositiveSmallIntegerField, ForeignKey, CASCADE
from django.urls import reverse

class Item(Model):
  class Meta:
    verbose_name = "Položka"
    default_related_name = "items"

  ITEM_CATEGORY = (
      ('N', 'Nápoje'),
      ('J', 'Jídlo'),
      ('O', 'Ostatní'),
      )

  name = CharField(max_length=51, unique=True, verbose_name="Název")
  price = PositiveSmallIntegerField(default=0, verbose_name="Cena")
  category = CharField(max_length=1, choices=ITEM_CATEGORY, default='N', verbose_name="Kategorie")
  pub = ForeignKey('Pub', on_delete=CASCADE, verbose_name="Hospoda")

  def __unicode__(self):
    return '%s' % self.name

  def get_absolute_url(self):
    return reverse('beercounter:pub', kwargs={'pk': self.pub.pk})

  def clean(self):
    self.name = self.name.capitalize()

class Bill(Model):
  class Meta:
    unique_together = ('name', 'pub')
    default_related_name = "bills"
    verbose_name = "Účet"

  name = CharField(max_length=50, verbose_name="Jméno")
  pub = ForeignKey('Pub', on_delete=CASCADE, )

  @property
  def spending(self):
    orders = self.orders.all()
    return sum([order.total_cost for order in orders])

  def __unicode__(self):
    return '%s' % self.name

  def clean(self):
    self.name = self.name.capitalize()

  def get_absolute_url(self):
    return reverse('beercounter:pub', kwargs={'pk': self.pub.pk})

class Pub(Model):
  class Meta:
    verbose_name = "Hospoda"

  name = CharField(max_length=50, unique=True, verbose_name="Název")

  def __unicode__(self):
    return '%s' % self.name

  def get_absolute_url(self):
    return reverse('beercounter:index')

  def clean(self):
    self.name = self.name.capitalize()

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
