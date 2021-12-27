from graphene_django import DjangoObjectType

from .models import Address, User, UserImage


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)


class UserImageType(DjangoObjectType):
    class Meta:
        model = UserImage


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
