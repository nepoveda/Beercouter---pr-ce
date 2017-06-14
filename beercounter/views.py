# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.db.models.functions import Lower
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpRequest

from .models import Pub, Bill, Order, Item
from .forms import ItemForm, BillForm

class IndexView(ListView):
  template_name = 'beercounter/index.html'
  context_object_name = 'pub_list'
  model = Pub
  queryset = Pub.objects.order_by(Lower('name'))

class PubView(DetailView):
  model = Pub

class BillView(DetailView):
  model = Bill

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

class DeletePubView(DeleteView):
  model = Pub
  success_url = reverse_lazy('beercounter:index')

def deleteItem(request, id):
  item = get_object_or_404(Item, pk=id).delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
