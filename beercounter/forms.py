from django.forms import ModelForm, CharField, HiddenInput
from django import forms

from .models import Item, Bill, Order

class ItemForm(ModelForm):
  class Meta:
    model = Item
    fields = '__all__'
    widgets = {
        'pub': forms.HiddenInput,
        }

class BillForm(ModelForm):
  class Meta:
    model = Bill
    fields = '__all__'
    widgets = {
        'pub': forms.HiddenInput,
        }

class OrderForm(ModelForm):
  class Meta:
    model = Order
    fields = '__all__'
    widgets ={
        'bill': HiddenInput,
        }

  def __init__(self, *args, **kwargs):
    super(OrderForm,self).__init__(*args, **kwargs)
    data = kwargs.get('initial', kwargs.get('data'))
    bill = Bill.objects.get(pk = data['bill'])

    self.fields['item'].queryset = \
      self.fields['item'].queryset.filter(pub_id = bill.pub_id)
