from graphene_django import DjangoObjectType

from .models import (
    Attribute, BusinessCard, BusinessCardImage, Brand,
    Category, Comment, Type, Product, SubProduct, SubProductImage, Stock
)


class BusinessCardType(DjangoObjectType):
    class Meta:
        model = BusinessCard
        fields = '__all__'


class BusinessCardImageType(DjangoObjectType):
    class Meta:
        model = BusinessCardImage
        fields = '__all__'


class BrandType(DjangoObjectType):
    class Meta:
        model = Brand
        fields = '__all__'


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'


class TypeNode(DjangoObjectType):
    class Meta:
        model = Type
        fields = '__all__'


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class SubProductType(DjangoObjectType):
    class Meta:
        model = SubProduct
        fields = '__all__'


class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = '__all__'


class AttributeType(DjangoObjectType):
    class Meta:
        model = Attribute
        fields = '__all__'


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = '__all__'


class SubProductImageType(DjangoObjectType):
    class Meta:
        model = SubProductImage
        fields = '__all__'
