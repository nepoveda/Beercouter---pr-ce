# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import ModelForm, CharField, HiddenInput, EmailField, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item, Bill, Order, Pub, Pub

class ItemForm(ModelForm):
  class Meta:
    model = Item
    exclude = ['owner', 'isBase']
    widgets = {
        'pub': HiddenInput,
        }

class BillForm(ModelForm):
  class Meta:
    model = Bill
    exclude = ['owner', 'isBase']
    widgets = {
        'pub': HiddenInput,
        }

class OrderForm(ModelForm):
  class Meta:
    model = Order
    fields = '__all__'
    widgets ={
        'bill': HiddenInput,
        }

  def __init__(self, *args, **kwargs):
    if kwargs:
      user = kwargs.pop('user')
    super(OrderForm,self).__init__(*args, **kwargs)
    if kwargs:
      bill = kwargs.get('instance', kwargs.get('bill'))
    else:
      bill=Bill.objects.get(pk=args[0]['bill'])
    self.fields['item'].queryset = \
        self.fields['item'].queryset.filter(pub_id = bill.pub_id)
    self.fields['item'].queryset = \
        self.fields['item'].queryset.filter(isBase=True) | self.fields['item'].queryset.filter(owner=user)

class PubForm(ModelForm):
  class Meta:
    model = Pub
    fields = ['name']

  def __init__(self, *args, **kwargs):
    super(PubForm, self).__init__(*args, **kwargs)
    self.fields['name'].widget.attrs.update({'class': "form-control"})

class SignUpForm(UserCreationForm):
  email = EmailField(max_length=254, help_text='Sem vám bude zaslán validační email, prosím vyplňte toto pole validním emailem, jinak se nebudete moci přihlásit')

  class Meta:
    model = User
    fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      raise ValidationError(u'Zdaný email je již použit')
    return email
