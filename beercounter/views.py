# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.db.models.functions import Lower
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpRequest

from .models import Pub, Bill, Order, Item
from .forms import ItemForm, BillForm, OrderForm

class IndexView(ListView):
  template_name = 'beercounter/index.html'
  context_object_name = 'pub_list'
  model = Pub
  queryset = Pub.objects.order_by(Lower('name'))

class PubView(DetailView):
  model = Pub

class BillView(UpdateView):
  template_name = 'beercounter/bill_update_form.html'
  model = Bill
  form_class = OrderForm

  def get_context_data(self, **kwargs):
    data = super(BillView, self).get_context_data(**kwargs)
    return data

  def get_form_kwargs(self,**kwargs):
    kwargs = super(BillView, self).get_form_kwargs(**kwargs)
    return kwargs

class AddPubView(CreateView):
  model = Pub
  fields = '__all__'


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

class OrderFormView(FormView):
  form_class = OrderForm
  template_name = 'beercounter/bill_update_form.html'
  success_url = 'beercounter:order'

  def post(self, request, *args, **kwargs):
    order_form = self.form_class(request.POST)
    if order_form.is_valid():
      print('proslo to')
      order_form.save()
      return self.render_to_response(
          self.get_context_data())

  def get_context_data(self,**kwargs):
    data = super(OrderFormView, self).get_context_data(**kwargs)
    data['bill'] = Bill.objects.get(pk=self.kwargs['pk'])
    return data

  def get_form_kwargs(self,**kwargs):
   kwargs = super(OrderFormView,self).get_form_kwargs(**kwargs)
   kwargs['initial']['bill'] = self.kwargs['pk']
   return kwargs

class DeletePubView(DeleteView):
  model = Pub
  success_url = reverse_lazy('beercounter:index')

def deleteItem(request, id):
  if request.method == 'POST':
    get_object_or_404(Item, pk=id).delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deleteBill(request, id):
  if request.method == 'POST':
    get_object_or_404(Bill, pk=id).delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
