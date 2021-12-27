from django.contrib import admin

from .models import (
    Attribute, BusinessCard, Brand, Category,
    Comment, Type, Product, SubProduct, Stock
)

admin.site.register(
    (Attribute, BusinessCard, Brand, Category,
     Comment, Type, Product, SubProduct, Stock,),
)
