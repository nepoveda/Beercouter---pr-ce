# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sys import maxint

from django.test import TestCase
from django.db import IntegrityError

from .models import *
from .forms import *
# Create your tests here.

class PubTest(TestCase):
  # "Test pub model"
  # fixtures = ['fixtures.json']

  def setUp(self):
    "Create test object"
    self.pub = Pub.objects.create(name = "TestPub")

  def test_unique(self):
    with self.assertRaises(IntegrityError):
      Pub.objects.create(name=self.pub.name)

  def test_absolute_url(self):
    self.assertEqual(self.pub.get_absolute_url(), reverse('beercounter:index'))

class BillTest(TestCase):

  def setUp(self):
    self.pub = Pub.objects.create(name = "TestPub")
    self.bill = self.pub.bills.create(name = "TestBill")

  def test_unique(self):
    with self.assertRaises(IntegrityError):
      self.pub.bills.create(name = "TestBill")

  def test_unique_together(self):
    bill2 = self.pub.bills.create(name = "TestBill2")
    pub2 = Pub.objects.create(name = "TestPub2")
    bill3 = pub2.bills.create(name = self.bill.name)


  def test_spending(self):
    item = self.pub.items.create(name="testitem", price=10)
    item2 = self.pub.items.create(name="testitem2", price=10)
    self.bill.orders.create(item = item, count=5)
    self.bill.orders.create(item = item2, count=2)
    self.assertEqual(self.bill.spending,70)


class ItemTest(TestCase):

  def setUp(self):
    self.pub = Pub.objects.create(name = "TestPub")
    self.item = self.pub.items.create(name = "testovacíItem", price=10, category="J")

  def test_item_unique(self):
    with self.assertRaises(IntegrityError):
      self.pub.items.create(name = self.item.name.encode('utf-8'), price = 10)

  def test_item_string_represantion(self):
    self.assertEqual(self.item.name, "testovacíItem".encode('utf-8').decode('utf-8'))

  def test_verbose_name(self):
    self.assertEqual(Item._meta.verbose_name.encode('utf-8'), "Položka".encode('utf-8'))

  def test_absolute_url(self):
    self.assertEqual(self.item.get_absolute_url(),
        reverse("beercounter:pub",kwargs={'pk':self.pub.pk}))

  def test_related_name(self):
    self.assertEqual(Item._meta.default_related_name.encode('utf-8'), 'items')


class OrderTest(TestCase):

  def setUp(self):
    self.pub = Pub.objects.create(name = "TestPub")
    self.item = self.pub.items.create(name = "TestItem", price = 10)
    self.bill = self.pub.bills.create(name = "TestBill")
    self.order = self.bill.orders.create(item = self.item, count = 5)

  def test_order_unique(self):
    with self.assertRaises(IntegrityError):
      self.bill.orders.create(item = self.item)

  def test_total_count(self):
    self.assertEqual(self.order.total_cost, 50)

class IndexViewTest(TestCase):

  def testPubList(self):
    Pub.objects.create(name = "Test1")
    Pub.objects.create(name = "Test3")
    Pub.objects.create(name = "Test2")
    response = self.client.get(reverse('beercounter:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context_data['pub_list'], ['<Pub: Test1>','<Pub: Test2>',
      '<Pub: Test3>'])

  def testAddPub(self):
    response = self.client.post(reverse('beercounter:index'), {'name': 'newPub'})
    self.assertEqual(response.status_code, 302)
    response = self.client.get(reverse('beercounter:index'))
    self.assertQuerysetEqual(response.context_data['pub_list'], ['<Pub: Newpub>'])
    #trying add again the same pub should return same Queryset
    response = self.client.post(reverse('beercounter:index'), {'name': 'newPub'})
    response = self.client.get(reverse('beercounter:index'))
    self.assertQuerysetEqual(response.context_data['pub_list'], ['<Pub: Newpub>'])


class PubViewTest(TestCase):

  def setUp(self):
    self.pub = Pub.objects.create(name = "TestPub")
    self.bill = self.pub.bills.create(name = "TestBill")
    self.item = self.pub.items.create(name = "TestItem")

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

  def setUp(self):
    self.pub   = Pub.objects.create(name      = "TestPub")
    self.bill  = self.pub.bills.create(name   = "TestBill")
    self.item  = self.pub.items.create(name   = "TestItem")
    self.item2 = self.pub.items.create(name   = "TestItem2")
    self.order = self.bill.orders.create(item = self.item, count=1)

  def test_get(self):
    response = self.client.get(reverse('beercounter:bill', args=[self.bill.id]))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context_data['object'], self.bill)

  def test_add_new_order(self):
    response = self.client.post(reverse('beercounter:bill', args=[self.bill.id]), {'addOrder': 'Přidat', 'item':str(self.item2.id), 'count': '3', 'bill':str(self.bill.id)})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(len(self.bill.orders.all()), 2)
    secondOrder = self.bill.orders.all()[1]
    self.assertEqual(secondOrder.count, 3)

  def test_add_existing_order(self):
    orderCount = self.order.count
    response = self.client.post(reverse('beercounter:bill', args=[self.bill.id]), {'addOrder':
      'Přidat', 'item':str(self.item.id), 'count': '3', 'bill':str(self.bill.id)})
    self.assertEqual(response.status_code, 302)
    self.order = Order.objects.get(pk=self.order.pk)
    self.assertEqual(self.order.count, orderCount + 3)

  def send_different_post(self):
    response = self.client.post(reverse('beercounter:bill', args=[self.bill.id]), {'addOrder':
      ''})
    self.assertEqual(response.status_code, 302)

class AddItemViewTest(TestCase):

  def setUp(self):
    self.pub = Pub.objects.create(name = "TestPub")

  def test_get(self):
    response = self.client.get(reverse('beercounter:additem', args=[self.pub.id]))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context_data['pubId'], str(self.pub.id))

class DecrementCountView(TestCase):

  def setUp(self):
    self.pub   = Pub.objects.create(name      = "TestPub")
    self.bill  = self.pub.bills.create(name   = "TestBill")
    self.item  = self.pub.items.create(name   = "TestItem")
    self.order = self.bill.orders.create(item = self.item, count=3)

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

  def setUp(self):
    self.pub   = Pub.objects.create(name      = "TestPub")
    self.bill  = self.pub.bills.create(name   = "TestBill")
    self.item  = self.pub.items.create(name   = "TestItem")
    self.item2  = self.pub.items.create(name   = "TestItem2")
    self.order = self.bill.orders.create(item = self.item, count=3)
    self.order2 = self.bill.orders.create(item = self.item2, count=3)

  def test_cleaning_orders(self):
    response = self.client.post(reverse("beercounter:cleanOrders"), {'bill': self.bill.id})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(len(self.bill.orders.all()) , 0)
