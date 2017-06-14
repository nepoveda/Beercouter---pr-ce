from django.conf.urls import url

from . import views

app_name = 'beercounter'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^pub/(?P<pk>[0-9]+)/$', views.PubView.as_view(), name="pub"),
    url(r'^pub/bill/(?P<pk>[0-9]+)/$', views.BillView.as_view(), name="bill"),
    url(r'^pub/add/$', views.AddPubView.as_view(), name="addpub"),
    url(r'^pub/(?P<pk>[0-9]+)/add/$', views.AddItemView.as_view(), name="additem"),
    url(r'^pub/(?P<pk>[0-9]+)/bill/$', views.AddBillView.as_view(), name="addbill"),
    url(r'^pub/delete/(?P<pk>[0-9]+)$', views.DeletePubView.as_view(), name="deletepub"),
    url(r'^pub/item/(?P<id>\d+)/$', views.deleteItem, name="deleteitem"),
    ]
