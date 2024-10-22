from django.urls import path

from . import views


app_name='cart'
urlpatterns=[
    path('view_cart',views.view_cart,name='view_cart'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('decrement/<int:id>',views.decrement,name='decrement'),
    path('remove/<int:id>',views.remove_cart,name='remove_cart'),
    path('place_order',views.orderform,name='place_order'),
    path('status/<u>',views.payment_status,name='payment_status'),
    path('my_orders',views.my_orders,name='my_orders')
]