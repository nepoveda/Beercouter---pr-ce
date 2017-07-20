#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts               import get_object_or_404, render, redirect
from django.views.generic           import ListView, DetailView, TemplateView
from django.views.generic.edit      import CreateView, DeleteView, UpdateView, FormView
from django.db.models.functions     import Lower
from django.urls                    import reverse, reverse_lazy
from django.http                    import HttpResponseRedirect, HttpRequest
from django.db.models               import F
from django.contrib.auth            import login, authenticate
from django.contrib.auth.forms      import UserCreationForm
from django.contrib.auth.models     import Group, User
from django.contrib.auth.tokens     import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http              import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding          import force_bytes, force_text
from django.template.loader         import render_to_string


from .models import Pub, Bill, Order, Item
from .forms import ItemForm, BillForm, OrderForm, PubForm, SignUpForm
from .task import send_validation_email

class IndexView(CreateView):
  model = Pub
  template_name = 'beercounter/index.html'
  form_class = PubForm

  def get_context_data(self, **kwargs):
    if self.request.user.is_staff:
      kwargs['pub_list'] = Pub.objects.all()
    elif self.request.user.is_active:
      kwargs['pub_list'] = Pub.objects.filter(isBase = True) | Pub.objects.filter(owner=self.request.user)
    else:
      kwargs['pub_list'] = Pub.objects.filter(isBase = True)
    return super(IndexView, self).get_context_data(**kwargs)

  def get_form_kwargs(self,**kwargs):
    kwargs = super(IndexView,self).get_form_kwargs(**kwargs)
    return kwargs

  def form_valid(self, form):
    form.instance.owner = self.request.user
    if self.request.user.is_staff:
      form.instance.isBase = True
    return super(IndexView, self).form_valid(form)

class PubView(DetailView):
  model = Pub

  def post(self, request, *args, **kwargs):

    if 'deleteBill' in request.POST:
      get_object_or_404(Bill, pk=request.POST.get("bill")).delete()

    if 'deleteItem' in request.POST:
      get_object_or_404(Item, pk=request.POST.get("item")).delete()

    return HttpResponseRedirect(reverse("beercounter:pub", args=[kwargs.get('pk')]))

  def get_context_data(self, **kwargs):
    kwargs['isOwner'] = self.object.isOwner(self.request.user)
    if self.request.user.is_authenticated:
      kwargs['bills'] = self.object.bills.filter(owner = self.request.user)
    data = super(PubView, self).get_context_data(**kwargs)
    return data

class BillView(DetailView):
  template_name = 'beercounter/bill_update_form.html'
  model = Bill


  def get_context_data(self,**kwargs):
    if self.request.user.is_active:
      items = self.object.pub.items.filter(owner = self.request.user) | self.object.pub.items.filter(isBase = True)
      kwargs['drinks'] = items.filter(category="N")
      kwargs['foods'] = items.filter(category="J")
      kwargs['others'] = items.filter(category="O")
    else:
      kwargs['items'] = self.object.pub.items.filter(owner = self.request.user)
    kwargs['orders'] = self.object.orders.all()
    data = super(BillView, self).get_context_data(**kwargs)
    return data

  # def get_form_kwargs(self,**kwargs):
  #   kwargs = super(BillView,self).get_form_kwargs(**kwargs)
  #   kwargs.update({'user': self.request.user})
  #   return kwargs

  # def form_valid(self, form):
  #   form.instance.owner = self.request.user
  #   form.instance.bill = self.object
  #   if self.request.user.is_staff:
  #     form.instance.isBase = True
  #   return super(BillView, self).form_valid(form)

  # def post(self, request, *args, **kwargs):
  #   self.object = self.get_object()
  #   form = self.form_class(request.POST, self.request.user)

  #   if 'addOrder' in request.POST:

  #     if form.is_valid():
  #       form.save()
  #       return self.form_valid(form)

  #     elif self.object.orders.filter(item_id = \
  #         form.cleaned_data['item'].id):
  #       order = get_object_or_404(self.object.orders.filter(item_id = \
  #           form.cleaned_data['item'].id))
  #       incrementOrderCount(order, form.cleaned_data['count'])
  #       return HttpResponseRedirect(reverse("beercounter:bill", args=[self.object.id]))

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

  def form_valid(self, form):
    form.instance.owner = self.request.user
    if self.request.user.is_staff:
      form.instance.isBase = True
    return super(AddItemView, self).form_valid(form)

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

  def form_valid(self, form):
    form.instance.owner = self.request.user
    if self.request.user.is_staff:
      form.instance.isBase = True
    return super(AddBillView, self).form_valid(form)

class DeletePubView(DeleteView):
  model = Pub
  success_url = reverse_lazy('beercounter:index')

class UpdateItemView(UpdateView):
  model = Item
  form_class = ItemForm
  template_name = 'beercounter/item_form.html'


  def get_context_data(self, **kwargs):
    data = super(UpdateItemView, self).get_context_data(**kwargs)
    self.object = self.get_object()
    data['pubId'] = self.object.pub_id
    return data

class UpdateBillView(UpdateView):
  model = Bill
  form_class = BillForm
  template_name = 'beercounter/bill_form.html'


  def get_context_data(self, **kwargs):
    data = super(UpdateBillView, self).get_context_data(**kwargs)
    self.object = self.get_object()
    data['pubId'] = self.object.pub_id
    return data

def createOrderView(request):
  item = get_object_or_404(Item, pk=request.POST['item'])
  bill = get_object_or_404(Bill, pk=request.POST['bill'])
  order, created = bill.orders.get_or_create(item=item, defaults={'count': request.POST['count']})
  if not created:
    incrementOrderCount(order, request.POST['count'])
  return redirect("beercounter:bill", bill.id)

def incrementOrderCount(order, count):
  order.count = F('count') + count
  order.save()
  order = Order.objects.get(pk=order.pk)

def incrementCount(request):
  order = get_object_or_404(Order,pk=request.POST['order'])
  incrementOrderCount(order, request.POST['count'])
  return HttpResponseRedirect(reverse("beercounter:bill", args=[request.POST['bill']]))

def decrementCount(request):
  order = get_object_or_404(Order,pk=request.POST['order'])
  if request.POST['count'] and order.count <= int(request.POST['count']):
    order.delete()
  else:
    order.count = F('count') - request.POST['count']
    order.save()
  return HttpResponseRedirect(reverse("beercounter:bill", args=[request.POST['bill']]))

def cleanOrders(request):
  get_object_or_404(Bill, pk=request.POST['bill']).orders.all().delete()
  return HttpResponseRedirect(reverse("beercounter:bill", args=[request.POST['bill']]))

class UpdateUserView(UpdateView):
  model = User
  fields = ['first_name', 'last_name', 'email']
  template_name = 'beercounter/user_form.html'
  success_url = reverse_lazy('beercounter:index')

  def get_object(self, queryset=None):
    return self.request.user

def signUp(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      token_generator = PasswordResetTokenGenerator()
      user = form.save()
      user.is_active = False
      user.groups.add(Group.objects.get(name="normal user"))
      user.save()
      current_site = get_current_site(request)
      subject = 'Beercounter aktivace'
      message = render_to_string("registration/activation_email.html",{
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        })
      # user.email_user(subject, message)
      send_validation_email.delay(user.id, subject, message)
      return HttpResponseRedirect(reverse("beercounter:useractivationsent"))
  else:
    form = SignUpForm()
  return render(request, "registration/signup.html", {"form": form})

def account_activation_sent(request):
  return render(request, "registration/account_activation_sent.html")

def activate(request, uidb64, token):
  token_generator = PasswordResetTokenGenerator()
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

  if user is not None and token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    login(request, user)
    return HttpResponseRedirect(reverse("beercounter:index"))
  else:
    return render(request, 'registration/account_activation_invalid.html')
