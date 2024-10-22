from django.urls import path
from . import views

app_name='booking'

urlpatterns=[
    # path('events',views.events,name='events'),
    path('reservation',views.reservation_form,name='reservation'),
    path('table_booking_slot',views.table_booking,name='table_booking_slot'),
    path('table_booking_status/<u>',views.payment_status,name='table_booking_status')
]

