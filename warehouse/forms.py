from cProfile import label
from dataclasses import fields
from distutils.text_file import TextFile
from inspect import Attribute
from pyexpat import model
from tkinter.tix import Select
from django import forms
from django.forms import widgets
from .models import Order, ShippingAddress

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
                    'pea_branch',
                    'pea_name',
                    'firstname',
                    'lastname',
                    'id_person',
                    'phone',
                    'product',
                    'order',
                    'address',
                ]
        labels = {
            'pea_branch': "รหัสการไฟฟ้า",
            'pea_name': "ชื่อการไฟฟ้า",
            'firstname': "ชื่อ",
            'lastname': "นามสกุล",
            'id_person': "รหัสพนักงาน",
            'phone': "เบอร์โทรศัพท์",
            'product': "สินค้า",
            'order': "จำนวน (ไม่เกิน 5)",
            'address': "ที่อยู่จัดส่ง",
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = "__all__"
        labels = {
            'pea_branch': "รหัสการไฟฟ้า",
            'pea_name': "ชื่อการไฟฟ้า",
            'firstname': "ชื่อ",
            'lastname': "นามสกุล",
            'id_person': "รหัสพนักงาน",
            'phone': "เบอร์โทรศัพท์",
            'product': "สินค้า",
            'bill': "ใบเสร็จ",
            'order_sold': "ยืนยันจำนวน",
        }