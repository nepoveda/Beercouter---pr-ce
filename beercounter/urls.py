from django.conf.urls import url

from . import views

app_name = 'beercounter'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^pub/(?P<pk>[0-9]+)/$', views.PubView.as_view(), name="pub"),
    url(r'^bill/(?P<pk>[0-9]+)/$', views.BillView.as_view(), name="bill"),
    url(r'^pub/(?P<pk>[0-9]+)/addItem/$', views.AddItemView.as_view(), name="additem"),
    url(r'^pub/(?P<pk>[0-9]+)/bill/$', views.AddBillView.as_view(), name="addbill"),
    url(r'^pub/delete/(?P<pk>[0-9]+)$', views.DeletePubView.as_view(), name="deletepub"),
    url(r'^item/update/(?P<pk>[0-9]+)$', views.UpdateItemView.as_view(), name="updateitem"),
    url(r'^bill/update/(?P<pk>[0-9]+)$', views.UpdateBillView.as_view(), name="updatebill"),
    url(r'^incrementCount/$', views.incrementCount, name="increment"),
    url(r'^decrementCount/$', views.decrementCount, name="decrement"),
    url(r'^cleanOrders/$', views.cleanOrders, name="cleanOrders"),
    ]
