from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
    url(r'^products/$', views.wall, name='product.wall'),
    url(r'^products/order/complete$', views.order_complete, name='product.order.complete'),
)
