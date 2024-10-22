from django.contrib import admin
from .models import Table_booking, Table_detail,Payment_table

admin.site.register(Table_booking)
admin.site.register(Table_detail)
admin.site.register(Payment_table)