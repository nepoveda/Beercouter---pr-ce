from django.forms import ModelForm, CharField, HiddenInput

from .models import Item, Bill, Order

class ItemForm(ModelForm):
  class Meta:
    model = Item
    fields = '__all__'
    widgets = {
        'pub': HiddenInput,
        }

class BillForm(ModelForm):
  class Meta:
    model = Bill
    fields = '__all__'
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
    super(OrderForm,self).__init__(*args, **kwargs)
    if kwargs:
      bill = kwargs.get('instance', kwargs.get('bill'))
      print self.fields['bill']
      self.fields['bill'] = bill
      print self.fields['bill']

    self.fields['item'].queryset = \
      self.fields['item'].queryset.filter(pub_id = bill.pub_id)
