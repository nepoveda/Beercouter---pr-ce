# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sys import maxint

from django.test import TestCase, RequestFactory
from django.db import IntegrityError

from .models import *
from .forms import *
from .views import *
# Create your tests here.

class PubTest(TestCase):
  # "Test pub model"
  fixtures = ['fixtures.json']

  def test_unique(self):
    with self.assertRaises(IntegrityError):
      Pub.objects.create(name="TestPub")

  def test_absolute_url(self):
    self.assertEqual(Pub.objects.first().get_absolute_url(), reverse('beercounter:index'))

class BillTest(TestCase):
  fixtures = ['fixtures.json']

  @classmethod
  def setUpTestData(cls):
    cls.pub = Pub.objects.get(name = "TestPub")
    cls.pub2 = Pub.objects.get(name = "TestPub2")
    cls.bill = cls.pub.bills.first()

  def test_unique(self):
    with self.assertRaises(IntegrityError):
      Bill.objects.create(name = "TestBill")

  def test_spending(self):
    item, item2 = self.pub.items.all()[0:2]
    self.bill.orders.create(item = item, count=5)
    self.bill.orders.create(item = item2, count=2)
    self.assertEqual(self.bill.spending,70)


class ItemTest(TestCase):
  fixtures = ['fixtures.json']

  @classmethod
  def setUpTestData(cls):
    cls.pub = Pub.objects.get(name = "TestPub")
    cls.item = cls.pub.items.get(name = "Testovacíitem")

  def test_item_unique(self):
    with self.assertRaises(IntegrityError):
      self.pub.items.create(name = self.item.name.encode('utf-8'), price = 10)

  def test_item_string_represantion(self):
    self.assertEqual(self.item.name, "Testovacíitem".encode('utf-8').decode('utf-8'))

  def test_verbose_name(self):
    self.assertEqual(Item._meta.verbose_name.encode('utf-8'), "Položka".encode('utf-8'))

  def test_absolute_url(self):
    self.assertEqual(self.item.get_absolute_url(),
        reverse("beercounter:pub",kwargs={'pk':self.pub.pk}))

  def test_related_name(self):
    self.assertEqual(Item._meta.default_related_name.encode('utf-8'), 'items')


class OrderTest(TestCase):
  fixtures = ['fixtures.json']

  @classmethod
  def setUpTestData(cls):
    cls.pub = Pub.objects.get(name = "TestPub")
    cls.item = cls.pub.items.get(name = "TestItem")
    cls.bill = cls.pub.bills.get(name = "TestBill")
    cls.order = cls.bill.orders.create(item = cls.item, count = 5)

  def test_order_unique(self):
    with self.assertRaises(IntegrityError):
      self.bill.orders.create(item = self.item)

  def test_total_count(self):
    self.assertEqual(self.order.total_cost, 50)

class IndexViewTest(TestCase):
  fixtures = ['fixtures']

  @classmethod
  def setUpTestData(cls):
    cls.factory = RequestFactory()
    cls.user = User.objects.get(username="user")

  def testPubList(self):
    request = self.factory.get(reverse('beercounter:index'))
    request.user = self.user
    response = IndexView.as_view()(request)
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context_data['pub_list'], ['<Pub: Testpub>','<Pub: Testpub2>',
      '<Pub: Testpub3>', '<Pub: Userpub>', '<Pub: Userpub2>'])

  def testAddPub(self):
    self.client.login(username="user", password="hesloheslo")
    response = self.client.post(reverse('beercounter:index'), {'name': 'newPub'})
    self.assertEqual(response.status_code, 302)
    response = self.client.get(reverse('beercounter:index'))
    self.assertTrue(Pub.objects.filter(name="newPub").exists())
    old_query_set = response.context_data['pub_list']


class PubViewTest(TestCase):
  fixtures = ['fixtures.json']

  @classmethod
  def setUpTestData(cls):
    cls.pub = Pub.objects.get(name = "TestPub")
    cls.bill = cls.pub.bills.get(name = "TestBill")
    cls.item = cls.pub.items.get(name = "TestItem")

  def test_get(self):
    response = self.client.get(reverse('beercounter:pub', args=[self.pub.id]))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context_data['object'], self.pub)

  def test_delete_item(self):
    response =  self.client.post(reverse('beercounter:pub', args = [self.pub.id]), {'item':
      str(self.item.id), 'deleteItem': ''})
    with self.assertRaises(Item.DoesNotExist):
      Item.objects.get(name="TestItem")

  def test_delete_bill(self):
    response = self.client.post(reverse('beercounter:pub', args = [self.pub.id]), {'bill':
      str(self.bill.id), 'deleteBill' : ''})
    with self.assertRaises(Bill.DoesNotExist):
      Bill.objects.get(name="TestBill")

  def test_deleting_bill_non_exist(self):
    response = self.client.post(reverse('beercounter:pub', args = [self.pub.id]), {'bill':
      str(maxint), 'deleteBill' : ''})
    self.assertEqual(response.status_code, 404)

  def test_deleting_item_non_exist(self):
    response = self.client.post(reverse('beercounter:pub', args = [self.pub.id]), {'item':
      str(maxint), 'deleteItem' : ''})
    self.assertEqual(response.status_code, 404)


class BillViewTest(TestCase):
  fixtures = ['fixtures.json']

  @classmethod
  def setUpTestData(cls):
    cls.pub   = Pub.objects.get(name      = "TestPub")
    cls.bill  = cls.pub.bills.get(name   = "TestBill")
    cls.item  = cls.pub.items.get(name   = "TestItem")
    cls.item2 = cls.pub.items.get(name   = "TestItem2")
    cls.order = cls.bill.orders.create(item = cls.item, count=1)

  def test_get(self):
    self.client.login(username="user", password="hesloheslo")
    response = self.client.get(reverse('beercounter:bill', args=[self.bill.id]))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context_data['object'], self.bill)

class AddItemViewTest(TestCase):
  fixtures = ['fixtures']

  @classmethod
  def setUpTestData(cls):
    cls.pub = Pub.objects.get(name = "TestPub")

  def test_get(self):
    self.client.login(username="user", password="hesloheslo")
    response = self.client.get(reverse('beercounter:additem', args=[self.pub.id]))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context_data['pubId'], str(self.pub.id))

class DecrementCountView(TestCase):
  fixtures = ['fixtures']

  @classmethod
  def setUpTestData(cls):
    cls.pub   = Pub.objects.get(name      = "TestPub")
    cls.bill  = cls.pub.bills.get(name   = "TestBill")
    cls.item  = cls.pub.items.get(name   = "TestItem")
    cls.order = cls.bill.orders.create(item = cls.item, count=3)

  def test_decremanting(self):
    original_count = self.order.count
    response = self.client.post(reverse("beercounter:decrement"), {'order': self.order.id,
      'count': 1, 'bill': self.bill.id})
    self.order = Order.objects.get(pk=self.order.pk)
    self.assertEqual(self.order.count, original_count - 1)

  def test_deleting_when_decremantion(self):
    original_orders_count = len(self.bill.orders.all())
    response = self.client.post(reverse("beercounter:decrement"), {'order': self.order.id,
      'count':'4', 'bill': self.bill.id})
    self.assertEqual(len(self.bill.orders.all()), original_orders_count - 1)

  def test_without_count(self):
    original_order_count = self.order.count
    response = self.client.post(reverse("beercounter:decrement"), {'order': self.order.id,
      'count':'', 'bill': self.bill.id})
    self.assertEqual(self.order.count, original_order_count)

class CleanOrdersView(TestCase):
  fixtures = ['fixtures']

  @classmethod
  def setUpTestData(cls):
    cls.pub    = Pub.objects.get(name      = "TestPub")
    cls.bill   = cls.pub.bills.get(name   = "TestBill")
    cls.item   = cls.pub.items.get(name   = "TestItem")
    cls.item2  = cls.pub.items.get(name   = "TestItem2")
    cls.order  = cls.bill.orders.create(item = cls.item, count  = 3)
    cls.order2 = cls.bill.orders.create(item = cls.item2, count = 3)

  def test_cleaning_orders(self):
    response = self.client.post(reverse("beercounter:cleanOrders"), {'bill': self.bill.id})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(len(self.bill.orders.all()) , 0)
