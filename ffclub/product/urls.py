from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns(
    '',
    url(r'^products/$', views.wall, name='product.wall'),
    url(r'^products/order/verify/$', views.order_verify, name='product.order.verify'),
    url(r'^products/order/complete/$', views.order_complete, name='product.order.complete'),

    # Currently use django admin for this
    # url(r'^products/add/$', views.add_product, name='product.add'),
)
