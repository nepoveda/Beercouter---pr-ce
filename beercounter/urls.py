from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

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
    url(r'^user/update/(?P<pk>[0-9]+)$', views.UpdateUserView.as_view(), name="updateuser"),
    url(r'^incrementCount/$', views.incrementCount, name="increment"),
    url(r'^decrementCount/$', views.decrementCount, name="decrement"),
    url(r'^createOrder/$', views.createOrderView, name="createorder"),
    url(r'^cleanOrders/$', views.cleanOrders, name="cleanOrders"),
    url('^', include('django.contrib.auth.urls')),
    url(r'^signUp/$', views.signUp, name="signup"),
    url(r'^account_activation_sent/$', views.account_activation_sent,
      name='useractivationsent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
              views.activate, name='activate'),
    ]
