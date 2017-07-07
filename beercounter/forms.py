from django.forms import ModelForm, CharField, HiddenInput

from .models import Item, Bill, Order, Pub, Pub

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
    else:
      bill=Bill.objects.get(pk=args[0]['bill'])
    self.fields['item'].queryset = \
        self.fields['item'].queryset.filter(pub_id = bill.pub_id)

class PubForm(ModelForm):
  class Meta:
    model = Pub
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(PubForm, self).__init__(*args, **kwargs)
    self.fields['name'].widget.attrs.update({'class': "form-control"})
