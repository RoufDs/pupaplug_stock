from django.contrib import admin
from django.db import models

# Register your models here.

from .models import register_member,Product , Order, ShippingAddress, Pea_branch


class register_member_admin (admin.ModelAdmin):
    # list_display = ("username", "company", "province")
    ordering = ['username__first_name']
    search_fields = ['username', 'member_type']


admin.site.register(register_member, register_member_admin)

admin.site.register(Pea_branch)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ShippingAddress)