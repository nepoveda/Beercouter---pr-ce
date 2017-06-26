#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.db.models.functions import Lower
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpRequest
from django.db.models import F

from .models import Pub, Bill, Order, Item
from .forms import ItemForm, BillForm, OrderForm

# class IndexView(ListView):
#   template_name = 'beercounter/index.html'
#   context_object_name = 'pub_list'
#   model = Pub
#   queryset = Pub.objects.order_by(Lower('name'))

class IndexView(CreateView):
  model = Pub
  fields = '__all__'
  template_name = 'beercounter/index.html'

  def get_context_data(self, **kwargs):
    kwargs['pub_list'] = Pub.objects.order_by(Lower('name'))
    return super(IndexView, self).get_context_data(**kwargs)

class PubView(DetailView):
  model = Pub

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()

    if 'deleteBill' in request.POST:
      get_object_or_404(Bill, pk=request.POST.get("bill")).delete()

    if 'deleteItem' in request.POST:
      get_object_or_404(Item, pk=request.POST.get("item")).delete()

    return HttpResponseRedirect(reverse("beercounter:pub", args=[kwargs.get('pk')]))

class BillView(UpdateView):
  template_name = 'beercounter/bill_update_form.html'
  model = Bill
  form_class = OrderForm


  def get_context_data(self,**kwargs):
    data = super(BillView, self).get_context_data(**kwargs)
    return data


  def get_form_kwargs(self,**kwargs):
    kwargs = super(BillView,self).get_form_kwargs(**kwargs)
    kwargs['initial']['bill'] = self.kwargs['pk']
    return kwargs

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = self.form_class(request.POST)

    if 'addOrder' in request.POST:

      if form.is_valid():
        form.save()
        return self.form_valid(form)

      elif self.object.orders.filter(item_id = \
          form.cleaned_data['item'].id):
        order = get_object_or_404(self.object.orders.filter(item_id = \
            form.cleaned_data['item'].id))
        order.count = F('count') + form.cleaned_data['count']
        order.save()
        return HttpResponseRedirect(reverse("beercounter:bill", args=[self.object.id]))



    else:
      return self.form_invalid()


class AddItemView(CreateView):
  form_class = ItemForm
  template_name = 'beercounter/item_form.html'

  def get_context_data(self, **kwargs):
    data = super(AddItemView, self).get_context_data(**kwargs)
    data['pubId'] = self.kwargs['pk']
    return data

  def get_form_kwargs(self,**kwargs):
    kwargs = super(AddItemView, self).get_form_kwargs(**kwargs)
    kwargs['initial']['pub'] = self.kwargs['pk']
    return kwargs

class AddBillView(CreateView):
  form_class = BillForm
  template_name = 'beercounter/bill_form.html'

  def get_context_data(self,**kwargs):
    data = super(AddBillView, self).get_context_data(**kwargs)
    data['pubId'] = self.kwargs['pk']
    return data

  def get_form_kwargs(self,**kwargs):
    kwargs = super(AddBillView, self).get_form_kwargs(**kwargs)
    kwargs['initial']['pub'] = self.kwargs['pk']
    return kwargs

class DeletePubView(DeleteView):
  model = Pub
  success_url = reverse_lazy('beercounter:index')

def incrementCount(request):
  order = Order.objects.get(pk=request.POST['order'])
  order.count = F('count') + request.POST['count']
  order.save()
  return HttpResponseRedirect(reverse("beercounter:bill", args=[request.POST['bill']]))

def decrementCount(request):
  order = Order.objects.get(pk=request.POST['order'])
  if request.POST['count'] and order.count <= int(request.POST['count']):
    order.delete()
  else:
    order.count = F('count') - request.POST['count']
    order.save()
  return HttpResponseRedirect(reverse("beercounter:bill", args=[request.POST['bill']]))

def cleanOrders(request):
  Bill.objects.get(pk=request.POST['bill']).orders.all().delete()
  return HttpResponseRedirect(reverse("beercounter:bill", args=[request.POST['bill']]))
