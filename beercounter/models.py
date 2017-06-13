# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Model, CharField, PositiveSmallIntegerField, ForeignKey, CASCADE
from django.urls import reverse

class Item(Model):
  ITEM_CATEGORY = (
      ('N', 'Nápoje'),
      ('J', 'Jídlo'),
      ('O', 'Ostatní'),
      )
  name = CharField(max_length=51, unique=True, verbose_name="Název")
  price = PositiveSmallIntegerField(default=0, verbose_name="Cena")
  category = CharField(max_length=1, choices=ITEM_CATEGORY, default='J', verbose_name="Kategorie")
  pub = ForeignKey('Pub', on_delete=CASCADE, related_name="items", verbose_name="Hospoda")

  def __unicode__(self):
    return ('%s' % self.name).encode('ascii', errors='replace')

  def get_absolute_url(self):
    return reverse('beercounter:pub', kwargs={'pk': self.pub.pk})

  def clean(self):
    self.name = self.name.capitalize()

class Bill(Model):
  class Meta:
    unique_together = ('name', 'pub')

  name = CharField(max_length=50, verbose_name="Jméno")
  pub = ForeignKey('Pub', on_delete=CASCADE, related_name="bills")

  def __unicode__(self):
    return ('%s' % self.name).encode('ascii', errors='replace')

  def clean(self):
    self.name = self.name.capitalize()

  def get_absolute_url(self):
    return reverse('beercounter:pub', kwargs={'pk': self.pub.pk})

class Pub(Model):
  name = CharField(max_length=50, unique=True, verbose_name="Název")

  def __unicode__(self):
    return ('%s' % self.name).encode('ascii', errors='replace')

  def get_absolute_url(self):
    return reverse('beercounter:index')

  def clean(self):
    self.name = self.name.capitalize()

class Order(Model):
  class Meta:
    unique_together = ('bill', 'item')
  bill = ForeignKey('Bill', on_delete=CASCADE, related_name="bill")
  item = ForeignKey('Item', on_delete=CASCADE, related_name="item")
  count = PositiveSmallIntegerField(default=0)
