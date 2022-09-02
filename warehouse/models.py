from distutils.command.upload import upload
from random import choices
from tkinter import N
from typing import Dict
from unicodedata import name
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.expressions import F
from django.db.models.fields import CharField, EmailField, IntegerField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.fields.related import ForeignKey

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from pkg_resources import require
from rest_framework import status

from django import forms

# Create your models here.

choice_member_type = [('1', 'admin'),
                      ('2', 'driver'),
                      ('3', 'entre'),
                      ('4', 'view_entre'),
                      ('0', '-')]


class register_member (models.Model):  # register all member & driver
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    # Admin, driver, share holder
    member_type = models.CharField(
        max_length=1, default='2', choices=choice_member_type)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    date_manual = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['username__first_name']

    def __str__(self):
        return "username {} || member_type  {}".format(self.username, choice_member_type[int(self.member_type)][1])

class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    countInStock = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    central = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    circulation = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class Pea_branch(models.Model):
    pea_branch  = models.CharField(max_length=200, null=False, blank=False, unique=True)
    pea_name = models.CharField(max_length=200, null=True, blank=True)
    product = models.CharField(max_length=200, null=False, blank=False)
    stock = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    circulation = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        self.pea_branch = self.pea_branch.upper()
        return super(Pea_branch, self).save(*args, **kwargs)

    def __str__(self):
        return self.pea_branch

class Order(models.Model):
    pea_branch = models.CharField(max_length=200, null=False, blank=False)
    pea_name = models.CharField(max_length=200, null=False, blank=False)
    firstname = models.CharField(max_length=200, blank=False, null=False)
    lastname = models.CharField(max_length=200, blank=False, null=False)
    id_person = models.CharField(max_length=200, null=False, blank=False)
    phone = models.IntegerField(null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    order = models.IntegerField(null=True, blank=True, default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    address = models.TextField(max_length=200, null=False, blank=False)
    createAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, blank=False, null=False, choices=(('pending','Pending'), ('finished','Finished'), ('missing','Missing')), default='pending')

    def save(self, *args, **kwargs):
        self.pea_branch = self.pea_branch.upper()
        self.id_person = self.id_person.upper()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pea_branch)


class ShippingAddress(models.Model):
    pea_branch = models.CharField(max_length=200, null=False, blank=False)
    pea_name = models.CharField(max_length=200, null=False, blank=False)
    firstname = models.CharField(max_length=200, blank=False, null=False)
    lastname = models.CharField(max_length=200, blank=False, null=False)
    id_person = models.CharField(max_length=200, null=False, blank=False)
    phone = models.IntegerField(null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    bill = models.ImageField(upload_to='bill', null=True, blank=True)
    order_sold = models.IntegerField(null=True, blank=True, default=1, validators=[MinValueValidator(1)])
    createAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.pea_branch = self.pea_branch.upper()
        self.id_person = self.id_person.upper()
        return super(ShippingAddress, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pea_branch)