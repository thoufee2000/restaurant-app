from django.contrib import admin
from .models import Cart,Order_table,Payment_table

admin.site.register(Cart)
admin.site.register(Order_table)
admin.site.register(Payment_table)