from ast import Num
from genericpath import exists
from itertools import product
from multiprocessing import context
import re
from turtle import st
from unicodedata import name
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from datetime import datetime, date, timedelta, timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
import pytz
import requests
import json
from django.http import JsonResponse
from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from decouple import config, Csv
import math
import csv
from .models import Product, Order, ShippingAddress

from warehouse.models import register_member, Order, Pea_branch, Product

from .forms import OrderForm, ShippingForm


tz = pytz.timezone('Asia/Bangkok')

# Create your views here.


# def pppscan(request):
#     chip_id = request.GET['code']

#     return redirect('https://demopupaplug.herokuapp.com/pupaplug/pppscan?code='+chip_id)

def index(request):
    pea_branch = Pea_branch.objects.all().order_by('-circulation')
    product = Product.objects.all()

    vars = {
        'pea_branch': pea_branch,
        'product': product,
    }
    return render(request, 'index.html', vars)


def order(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)

        if form.is_valid():
            
            form.save()
            messages.success(request, "ทำรายการสำเร็จ")
            # print(form['product'])

            order_pea = form.cleaned_data.get('pea_branch')
            order_product = form.cleaned_data.get('product')
            order_order = form.cleaned_data.get('order')

            if Pea_branch.objects.filter(pea_branch=order_pea, product=order_product).exists():
                # pea_branchEditable
                Pea_model = Pea_branch.objects.get(pea_branch=order_pea, product=order_product)
                Pea_model.stock = Pea_model.stock + int(order_order)
                Pea_model.save()

                # productEditable
                Product_model = Product.objects.get(name=order_product)
                Product_model.countInStock = Product_model.countInStock - int(order_order)
                Product_model.central = Product_model.central + int(order_order)
                Product_model.save()

            else:
                Pea_branch.objects.create(pea_branch=order_pea, product=order_product, stock=order_order)

                # productEditable
                Product_model = Product.objects.get(name=order_product)
                Product_model.countInStock = Product_model.countInStock - int(order_order)
                Product_model.central = Product_model.central + int(order_order)
                Product_model.save()

        else:
            messages.error(request, "ทำรายการไม่สำเร็จ")

        return redirect('order')

    vars = {
        'form': OrderForm(),
        'products': products
    }
    return render(request, 'order.html', vars)


def receipt(request):
    if request.method == 'POST':
        form = ShippingForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกข้อมูลสำเร็จ")

            receipt_pea = form.cleaned_data.get('pea_branch')
            receipt_pean = form.cleaned_data.get('pea_name')
            receipt_product = form.cleaned_data.get('product')
            receipt_sold = form.cleaned_data.get('order_sold')

            receipt_first = form.cleaned_data.get('firstname')
            receipt_last = form.cleaned_data.get('lastname')
            receipt_iP = form.cleaned_data.get('id_person')
            receipt_phone = form.cleaned_data.get('phone')

            if Pea_branch.objects.filter(pea_branch=receipt_pea, product=receipt_product).exists():
                # pea_branchEditable
                Pea_model = Pea_branch.objects.get(pea_branch=receipt_pea, product=receipt_product)
                Product_model = Product.objects.get(name=receipt_product)
                if Pea_model.stock - int(receipt_sold) >= 0:
                    Pea_model.stock = Pea_model.stock - int(receipt_sold)
                    Pea_model.circulation = Pea_model.circulation + int(receipt_sold)
                    Pea_model.save()
                    
                    Product_model.central = Product_model.central - int(receipt_sold)
                    Product_model.circulation = Product_model.circulation + int(receipt_sold)
                    Product_model.save()

                else:
                    Product_model.countInStock = Product_model.countInStock - abs(Pea_model.stock - int(receipt_sold))
                    Product_model.central = Product_model.central - Pea_model.stock
                    Product_model.circulation = Product_model.circulation + Pea_model.stock + abs(Pea_model.stock - int(receipt_sold))
                    Product_model.save()

                    Order.objects.create(
                        pea_branch=receipt_pea,
                        pea_name=receipt_pean,
                        firstname=receipt_first,
                        lastname=receipt_last,
                        id_person=receipt_iP,
                        phone=receipt_phone,
                        product=receipt_product,
                        order=abs(Pea_model.stock - int(receipt_sold)),
                        address="กรุณาติดต่อทางเบอร์โทรศัพท์...",
                        status="missing"
                    )

                    Pea_model.stock = 0
                    Pea_model.circulation = Pea_model.circulation + int(receipt_sold)
                    Pea_model.save()

            else:
                messages.error(request, "มีข้อมูลไม่ถูกต้อง")

        else:
            messages.error(request, "บันทึกข้อมูลไม่สำเร็จ")

        return redirect('receipt')

    vars = {
        'form': ShippingForm()
    }

    return render(request, 'receipt.html', vars)


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            return redirect('admin')

        else:
            return redirect('loginForm')

    return render(request, 'loginForm.html')


def log_admin_out(request):
    logout(request)
    return redirect('index')


@login_required(login_url='admin_login')
def admin(request):
    pea_branch = Pea_branch.objects.all()
    product = Product.objects.all()
    order_pending = Order.objects.filter(status="pending")
    order_finished = Order.objects.filter(status="finished")
    order_missing = Order.objects.filter(status="missing")
    receipt_bill = ShippingAddress.objects.all()

    vars = {
        "pea_branch": pea_branch,
        "product": product,
        "pending": order_pending,
        "finished": order_finished,
        "missing": order_missing,
        "receipt": receipt_bill,
    }

    return render(request, 'admin.html', vars)


def pea_editable(request, id):
    pea_branch = Pea_branch.objects.get(id=id)

    if request.method == 'POST':
        pea_branch.pea_name = request.POST.get('pea_name')
        pea_branch.stock = request.POST.get('stock')
        pea_branch.circulation = request.POST.get('circulation')
        pea_branch.save()

        messages.success(request, "แก้ไขข้อมูลสำเร็จ")

        return redirect('admin')

    vars = {
        "pea_branch": pea_branch,
    }

    return render(request, 'peaEditable.html', vars)

def pea_delete(request, id):
    pea_branch = Pea_branch.objects.get(id=id)

    if request.method == 'POST':
        pea_branch.delete()

        messages.success(request, "ลบข้อมูลสำเร็จ")

        return redirect('admin')

    vars = {
        "pea_branch": pea_branch,
    }

    return render(request, 'peaDelete.html', vars)


def product_editable(request, id):
    productEditable = Product.objects.get(id=id)

    if request.method == 'POST':
        productEditable.countInStock = request.POST.get('stock')
        productEditable.central = request.POST.get('central')
        productEditable.circulation = request.POST.get('circulation')
        productEditable.save()

        messages.success(request, "แก้ไขข้อมูลสำเร็จ")

        return redirect('admin')

    vars = {
        "product": productEditable,
    }

    return render(request, 'productEditable.html', vars)


def product_delete(request, id):
    productDelete = Product.objects.get(id=id)

    if request.method == 'POST':
        productDelete.delete()

        messages.success(request, "ลบข้อมูลสำเร็จ")

        return redirect('admin')

    vars = {
        "product": productDelete,
    }

    return render(request, 'productDelete.html', vars)


def order_editable(request, id):
    orderEditable = Order.objects.get(id=id)

    if request.method == 'POST':
        orderEditable.status = request.POST.get('status')
        orderEditable.save()

        messages.success(request, "แก้ไขข้อมูลสำเร็จ")

        return redirect('admin')

    vars = {
        "order": orderEditable,
    }

    return render(request, 'orderEditable.html', vars)


def order_delete(request, id):
    orderEditable = Order.objects.get(id=id)

    if request.method == 'POST':
        orderEditable.delete()

        messages.success(request, "ลบข้อมูลสำเร็จ")

        return redirect('admin')

    vars = {
        "order": orderEditable,
    }

    return render(request, 'orderDelete.html', vars)


def receipt_editable(request, id):
    receiptEditable = ShippingAddress.objects.get(id=id)

    if request.method == 'POST':
        receiptEditable.order_sold = request.POST.get('order_sold')
        receiptEditable.save()

        messages.success(request, "แก้ไขข้อมูลสำเร็จ")

        return redirect('admin')

    vars = {
        "receipt": receiptEditable,
    }

    return render(request, 'receiptEditable.html', vars)


def receipt_delete(request, id):
    receiptEditable = ShippingAddress.objects.get(id=id)

    if request.method == 'POST':        
        receiptEditable.delete()

        messages.success(request, "แก้ไขข้อมูลสำเร็จ")

        return redirect('admin')

    vars = {
        "receipt": receiptEditable,
    }

    return render(request, 'receiptDelete.html', vars)