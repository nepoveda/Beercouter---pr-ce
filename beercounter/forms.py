from django.forms import ModelForm
from django import forms

from .models import Item, Bill

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
