import graphene
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from graphene_file_upload.scalars import Upload

from backend.permissions import (
    get_query, is_authenticated, paginate
)
from .inputs import (
    AttributeInput, BusinessCardInput, BrandInput, CategoryInput,
    CommentInput, TypeInput, ProductInput, SubProductInput, StockInput
)
from .models import (
    Attribute, Brand, BusinessCard, BusinessCardImage, Category,
    Comment, Product, SubProduct, Stock, Type, SubProductImage
)
from .tools import (
    ProductData
)
from .types import (
    BusinessCardType, BusinessCardImageType, BrandType, CategoryType, TypeNode,
    CommentType, ProductType, SubProductType, StockType, AttributeType, SubProductImageType
)


class CreateBusinessCard(graphene.Mutation):
    """Creating a business card for the user."""
    business_card = graphene.Field(BusinessCardType)

    class Arguments:
        business_card_data = BusinessCardInput(required=True)

    @is_authenticated
    def mutate(self, info, business_card_data):
        business_card = BusinessCard.objects.create(
            user=info.context.user,
            **business_card_data
        )

        return CreateBusinessCard(
            business_card=business_card
        )


class UpdateBusinessCard(graphene.Mutation):
    """Updating the user's business card."""
    business_card = graphene.Field(BusinessCardType)

    class Arguments:
        business_card_data = BusinessCardInput(required=True)

    @is_authenticated
    def mutate(self, info, business_card_data):
        try:
            business_card_id = info.context.user.business_card.id
        except Exception:
            raise Exception("You doesn't have a business card to update!")

        BusinessCard.objects.filter(
            id=business_card_id
        ).update(**business_card_data)

        return UpdateBusinessCard(
            business_card=BusinessCard.objects.get(id=business_card_id)
        )


class DeleteBusinessCard(graphene.Mutation):
    """Deleting a business card."""
    status = graphene.Boolean()

    @is_authenticated
    def mutate(self, info):
        BusinessCard.objects.filter(
            user=info.context.user
        ).delete()

        return DeleteBusinessCard(status=True)


class BusinessCardImageUpload(graphene.Mutation):
    """Uploading an image for business card page."""
    image = graphene.Field(BusinessCardImageType)

    class Arguments:
        image = Upload(required=True)
        alt_text = graphene.String()

    @is_authenticated
    def mutate(self, info, **kwargs):
        image = BusinessCardImage.objects.filter(
            card=info.context.user.business_card
        ).first()

        if image:
            image.delete()

        image = BusinessCardImage.objects.create(
            card=info.context.user.user_business_card,
            **kwargs
        )

        return BusinessCardImage(
            image=image
        )


class CreateProduct(graphene.Mutation):
    """Creating a product."""
    product = graphene.Field(ProductType)
    status = graphene.Boolean()

    class Arguments:
        brands = graphene.List(BrandInput, required=True)
        categories = graphene.List(CategoryInput, required=True)
        type = TypeInput(required=True)
        product_data = ProductInput(required=True)

    @is_authenticated
    def mutate(self, info, brands, categories, type, product_data):
        try:
            business_card = info.context.user.business_card
        except Exception:
            raise Exception("You don't have a business card to create product!")

        have_product = Product.objects.filter(
            card=business_card,
            name=product_data.get('name')
        )

        if have_product:
            raise Exception("You already have a product with this name!")

        brands = ProductData.get_brands(product_data=brands)
        categories = ProductData.get_categories(product_data=categories)
        product_type = ProductData.get_type(product_data=type)

        if not brands:
            raise Exception(_("Brand input field empty! Enter an existing brands!"))

        if not categories:
            raise Exception(_("Category input field empty! Enter an existing categories!"))

        product_instance = Product.objects.create(
            card=business_card,
            type=product_type,
            **product_data
        )

        product_instance.brand.set(brands)
        product_instance.category.set(categories)

        return CreateProduct(
            product=product_instance,
            status=True
        )


class UpdateProduct(graphene.Mutation):
    """Updating a product."""
    product = graphene.Field(ProductType)
    status = graphene.Boolean()

    class Arguments:
        product_id = graphene.ID(required=True)
        brands = graphene.List(BrandInput, required=True)
        categories = graphene.List(CategoryInput, required=True)
        type = TypeInput(required=True)
        product_data = ProductInput(required=True)

    @is_authenticated
    def mutate(self, info, brands, categories, type, product_data, product_id):
        try:
            business_card = info.context.user.business_card
        except Exception:
            raise Exception("You don't have a business card to create product!")

        try:
            Product.objects.get(id=product_id, card=business_card)
        except Product.DoesNotExist:
            return Exception("Create product before update!")

        have_product = Product.objects.filter(
            card=business_card,
            name=product_data.get('name')
        ).exclude(id=product_id)

        if have_product:
            raise Exception("You already have a product with this name")

        brands = ProductData.get_brands(product_data=brands)
        categories = ProductData.get_categories(product_data=categories)
        product_type = ProductData.get_type(product_data=type)

        if not brands:
            raise Exception(_("Brand input field empty! Enter an existing brands!"))

        if not categories:
            raise Exception(_("Category input field empty! Enter an existing categories!"))

        Product.objects.filter(
            id=product_id,
        ).update(
            **product_data,
            type=product_type
        )

        product_instance = Product.objects.get(id=product_id)
        product_instance.brand.clear()
        product_instance.brand.set(brands)
        product_instance.category.clear()
        product_instance.category.set(categories)

        return UpdateProduct(
            product=product_instance,
            status=True
        )


class DeleteProduct(graphene.Mutation):
    """Deleting a product."""
    status = graphene.Boolean()

    class Arguments:
        product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, product_id):
        Product.objects.filter(
            id=product_id,
            card=info.context.user.business_card
        ).delete()

        return DeleteProduct(
            status=True
        )


class CreateSubProduct(graphene.Mutation):
    """Creating a sub-product."""
    sub_product = graphene.Field(SubProductType)
    status = graphene.Boolean()

    class Arguments:
        product_id = graphene.ID(required=True)
        sub_product_data = SubProductInput(required=True)

    @is_authenticated
    def mutate(self, info, product_id, sub_product_data):
        try:
            business_card = info.context.user.business_card
        except Exception:
            raise Exception("You don't have a business card to create sub-product!")

        try:
            Product.objects.get(id=product_id, card=business_card)
        except Product.DoesNotExist:
            return Exception("Create product before creating sub-product!")

        have_sub_product = SubProduct.objects.filter(
            product_id=product_id,
            sku=sub_product_data.get('sku')
        )
        if have_sub_product:
            raise Exception("You already have a sub-product with this product code")

        sub_product_instance = SubProduct.objects.create(
            product_id=product_id,
            **sub_product_data
        )

        return CreateSubProduct(
            sub_product=sub_product_instance,
            status=True
        )


class UpdateSubProduct(graphene.Mutation):
    """Updating a sub-product."""
    sub_product = graphene.Field(SubProductType)
    status = graphene.Boolean()

    class Arguments:
        product_id = graphene.ID(required=True)
        sub_product_id = graphene.ID(required=True)
        sub_product_data = SubProductInput(required=True)

    @is_authenticated
    def mutate(self, info, product_id, sub_product_id, sub_product_data):
        try:
            business_card = info.context.user.business_card
        except Exception:
            raise Exception("You don't have a business card to create sub-product!")

        try:
            Product.objects.get(id=product_id, card=business_card)
        except Product.DoesNotExist:
            return Exception("Create a product before updating sub-product!")

        try:
            SubProduct.objects.get(id=sub_product_id, product_id=product_id)
        except SubProduct.DoesNotExist:
            return Exception("Create a sub-product before updating!")

        have_sub_product = SubProduct.objects.filter(
            product_id=product_id,
            sku=sub_product_data.get('sku')
        ).exclude(
            id=sub_product_id
        )
        if have_sub_product:
            raise Exception("You already have a sub-product with this product code")

        SubProduct.objects.filter(id=sub_product_id).update(
            **sub_product_data
        )

        return UpdateSubProduct(
            sub_product=SubProduct.objects.get(id=sub_product_id),
            status=True
        )


class DeleteSubProduct(graphene.Mutation):
    """Deleting a sub-product."""
    status = graphene.Boolean()

    class Arguments:
        product_id = graphene.ID(required=True)
        sub_product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, product_id, sub_product_id):
        SubProduct.objects.filter(
            id=sub_product_id,
            product_id=product_id
        ).delete()

        return DeleteSubProduct(status=True)


class CreateStock(graphene.Mutation):
    """Creating a stock."""
    stock = graphene.Field(StockType)
    status = graphene.Boolean()

    class Arguments:
        sub_product_id = graphene.ID(required=True)
        stock_data = StockInput(required=True)

    @is_authenticated
    def mutate(self, info, sub_product_id, stock_data):
        try:
            info.context.user.business_card
        except Exception:
            raise Exception("You don't have a business card to create sub-product!")

        try:
            sub_product = SubProduct.objects.get(id=sub_product_id)
        except Product.DoesNotExist:
            return Exception("Create a sub-product before creating stock!")

        have_stock = Stock.objects.filter(sub_product=sub_product)
        if have_stock:
            raise Exception("You already have a stock with this sub-product!")

        stock_instance = Stock.objects.create(
            sub_product_id=sub_product_id,
            **stock_data
        )

        return CreateStock(
            stock=stock_instance,
            status=True
        )


class UpdateStock(graphene.Mutation):
    """Updating a stock."""
    stock = graphene.Field(StockType)
    status = graphene.Boolean()

    class Arguments:
        sub_product_id = graphene.ID(required=True)
        stock_id = graphene.ID(required=True)
        stock_data = StockInput(required=True)

    @is_authenticated
    def mutate(self, info, sub_product_id, stock_id, stock_data):
        try:
            info.context.user.business_card
        except Exception:
            raise Exception("You don't have a business card to create sub-product!")

        try:
            SubProduct.objects.get(id=sub_product_id)
        except Product.DoesNotExist:
            return Exception("Create a sub-product before creating stock!")

        try:
            Stock.objects.get(id=stock_id, sub_product_id=sub_product_id)
        except Stock.DoesNotExist:
            return Exception("Create stock before updating!")

        Stock.objects.filter(id=stock_id).update(**stock_data)

        return UpdateStock(
            stock=Stock.objects.get(id=stock_id),
            status=True
        )


class DeleteStock(graphene.Mutation):
    """Deleting a stock."""
    status = graphene.Boolean()

    class Arguments:
        stock_id = graphene.ID(required=True)
        sub_product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, stock_id, sub_product_id):
        Stock.objects.filter(
            id=stock_id,
            sub_product_id=sub_product_id
        ).delete()

        return DeleteStock(status=True)


class CreateAttribute(graphene.Mutation):
    """Creating an attribute."""
    attribute = graphene.Field(AttributeType)
    status = graphene.Boolean()

    class Arguments:
        attribute_data = AttributeInput(required=True)
        sub_product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, attribute_data, sub_product_id):
        try:
            info.context.user.business_card
        except Exception:
            raise Exception("You don't have a business card to create sub-product!")

        try:
            sub_product = SubProduct.objects.get(id=sub_product_id)
        except SubProduct.DoesNotExist:
            return Exception("Create a sub-product before creating attribute!")

        have_attribute = Attribute.objects.filter(
            sub_product_id=sub_product_id,
            name=attribute_data.get('name'),
            value=attribute_data.get('value')
        )
        if have_attribute:
            raise Exception("You already have that attributes with this sub-product!")

        attribute_instance = Attribute.objects.create(
            sub_product_id=sub_product_id, **attribute_data
        )

        return CreateAttribute(attribute=attribute_instance, status=True)


class UpdateAttribute(graphene.Mutation):
    """Updating an attribute."""
    attribute = graphene.Field(AttributeType)
    status = graphene.Boolean()

    class Arguments:
        attribute_data = AttributeInput(required=True)
        attribute_id = graphene.ID(required=True)
        sub_product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, attribute_data, attribute_id, sub_product_id):
        try:
            info.context.user.business_card
        except Exception:
            raise Exception("You don't have a business card to create sub-product!")

        try:
            sub_product = SubProduct.objects.get(id=sub_product_id)
        except SubProduct.DoesNotExist:
            return Exception("Create a sub-product and his attribute before updating!")

        try:
            attribute = Attribute.objects.get(id=attribute_id)
        except Attribute.DoesNotExist:
            return Exception("Creating a attribute before updating!")

        have_attribute = Attribute.objects.filter(
            sub_product_id=sub_product_id,
            name=attribute_data.get('name'),
            value=attribute_data.get('value')
        ).exclude(id=attribute_id)
        if have_attribute:
            raise Exception("You already have that attributes with this sub-product!")

        Attribute.objects.filter(id=attribute_id).update(**attribute_data)

        return UpdateAttribute(attribute=Attribute.objects.get(id=attribute_id), status=True)


class DeleteAttribute(graphene.Mutation):
    """Deleting an attribute."""
    status = graphene.Boolean()

    class Arguments:
        attribute_id = graphene.ID(required=True)
        sub_product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, attribute_id, sub_product_id):
        Attribute.objects.filter(
            id=attribute_id, sub_product_id=sub_product_id
        ).delete()

        return DeleteAttribute(status=True)


class CreateComment(graphene.Mutation):
    """Creating a comment."""
    comment = graphene.Field(CommentType)
    status = graphene.Boolean()

    class Arguments:
        comment_data = CommentInput(required=True)
        sub_product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, comment_data, sub_product_id):
        business_card = info.context.user.business_card
        user_id = info.context.user.id

        if business_card:
            own_sub_product = SubProduct.objects.filter(
                id=sub_product_id, product__card=business_card
            )
            if own_sub_product:
                raise Exception("You can't comment on own product!")

        have_comment = Comment.objects.filter(user_id=user_id, sub_product_id=sub_product_id)

        if have_comment.exists():
            raise Exception("You have already reviewed this product!")

        comment_instance = Comment.objects.create(
            sub_product_id=sub_product_id,
            user_id=user_id, **comment_data
        )

        return CreateComment(status=True, comment=comment_instance)


class UpdateComment(graphene.Mutation):
    """Updating a comment."""
    comment = graphene.Field(CommentType)
    status = graphene.Boolean()

    class Arguments:
        comment_data = CommentInput(required=True)
        comment_id = graphene.ID(required=True)
        sub_product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, comment_id, comment_data, sub_product_id):
        try:
            Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise Exception(_("Create comment before update!"))

        Comment.objects.filter(
            id=comment_id, user__id=info.context.user.id, sub_product_id=sub_product_id
        ).update(**comment_data)

        return UpdateComment(
            comment=Comment.objects.get(id=comment_id),
            status=True
        )


class DeleteComment(graphene.Mutation):
    """Deleting a comment."""
    status = graphene.Boolean()

    class Arguments:
        comment_id = graphene.ID(required=True)
        sub_product_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, comment_id, sub_product_id):
        Comment.objects.filter(
            id=comment_id, user__id=info.context.user.id, sub_product_id=sub_product_id
        ).delete()
        return DeleteComment(status=True)


class CreateSubProductImage(graphene.Mutation):
    """Creating sub-product's image"""
    image = graphene.Field(SubProductImageType)
    status = graphene.Boolean()

    class Arguments:
        sub_product_id = graphene.ID(required=True)
        image = Upload(required=True)
        alt_text = graphene.String()

    @is_authenticated
    def mutate(self, info, sub_product_id, **kwargs):
        image = SubProductImage.objects.create(
            sub_product_id=sub_product_id,
            **kwargs
        )

        return CreateSubProductImage(
            image=image,
            status=True
        )


class UpdateSubProductImage(graphene.Mutation):
    """Updating sub-product's image"""
    image = graphene.Field(SubProductImageType)
    status = graphene.Boolean()

    class Arguments:
        image_id = graphene.ID(required=True)
        sub_product_id = graphene.ID(required=True)
        image = Upload(required=True)
        alt_text = graphene.String()

    @is_authenticated
    def mutate(self, info, image_id, sub_product_id, **kwargs):

        try:
            image = SubProductImage.objects.get(id=image_id, sub_product_id=sub_product_id)
        except SubProductImage.DoesNotExist:
            return Exception(_('Creating a image before updating!'))

        image.delete()

        image = SubProductImage.objects.create(sub_product_id=sub_product_id, **kwargs)

        return UpdateSubProductImage(
            image=image,
            status=True
        )


class DeletingSubProductImage(graphene.Mutation):
    """Deleting sub-product's image"""
    status = graphene.Boolean()

    class Arguments:
        image_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, image_id):
        SubProductImage.objects.filter(id=image_id).delete()

        return DeletingSubProductImage(
            status=True
        )


class Mutation(graphene.ObjectType):
    create_business_card = CreateBusinessCard.Field()
    update_business_card = UpdateBusinessCard.Field()
    delete_business_card = DeleteBusinessCard.Field()

    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

    create_sub_product = CreateSubProduct.Field()
    update_sub_product = UpdateSubProduct.Field()
    delete_sub_product = DeleteSubProduct.Field()

    create_stock = CreateStock.Field()
    update_stock = UpdateStock.Field()
    delete_stock = DeleteStock.Field()

    create_attribute = CreateAttribute.Field()
    update_attribute = UpdateAttribute.Field()
    delete_attribute = DeleteAttribute.Field()

    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()

    create_sub_product_image = CreateSubProductImage.Field()
    update_sub_product_image = UpdateSubProductImage.Field()
    delete_sub_product_image = DeletingSubProductImage.Field()

    card_image_upload = BusinessCardImageUpload.Field()


class Query(graphene.ObjectType):
    brands = graphene.List(
        BrandType,
        name=graphene.String(),
        description='Response data about existing brands.'
    )

    @staticmethod
    def resolve_brands(cls, info, name=False):
        query = Brand.objects.prefetch_related('product_brands')

        if name:
            query = query.filter(Q(name__icontains=name) | Q(name__iexact=name)).distinct()

        return query

    categories = graphene.List(
        CategoryType,
        name=graphene.String(),
        description='Response data about existing categories.'
    )

    @staticmethod
    def resolve_categories(cls, info, name=False):
        query = Category.objects.prefetch_related('product_categories')

        if name:
            query = query.filter(Q(name__icontains=name) | Q(name__iexact=name)).distinct()

        return query

    types = graphene.List(
        TypeNode,
        name=graphene.String(),
        description='Response data about existing types.'
    )

    @staticmethod
    def resolve_types(cls, info, name=False):
        query = Type.objects.prefetch_related('product_types')

        if name:
            query = query.filter(Q(name__icontains=name) | Q(name__iexact=name)).distinct()

        return query

    products = graphene.Field(
        paginate(ProductType), search=graphene.String(), min_price=graphene.Float(),
        max_price=graphene.Float(), brand=graphene.String(), category=graphene.String(),
        type_of_product=graphene.String(), business_card=graphene.String(), sort_by=graphene.String(),
        is_asc=graphene.Boolean(), mine=graphene.Boolean(), min_rating=graphene.Float(),
        max_rating=graphene.Boolean(), description='Response data paginated about existing products.'
    )

    @staticmethod
    def resolve_products(cls, info, **kwargs):

        mine = kwargs.get('mine', False)
        if mine and not info.context.user:
            raise Exception('User auth required!')

        query = Product.objects.select_related('card', 'type').prefetch_related(
            'brand', 'category', 'sub_product', 'sub_product__attributes',
            'sub_product__comments', 'sub_product__stock'
        )

        if mine:
            query = query.filter(card_id=info.context.user.id)

        if kwargs.get('search', None):
            qs = kwargs['search']
            search_fields = (
                'name', 'description'
            )
            search_data = get_query(qs, search_fields)
            query = query.filter(search_data)

        if kwargs.get('min_price', None):
            qs = kwargs['min_price']
            q = Product.objects.filter(sub_product__sale_price__qt=qs)

            query = query.filter(Q(sub_product__sale_price__qt=qs) | Q(sub_product__sale_price=qs)).distinct()

        if kwargs.get('max_price', None):
            qs = kwargs['max_price']
            query = query.filter(Q(sub_product__sale_price__lt=qs) | Q(sub_product__sale_price=qs)).distinct()

        if kwargs.get('brand', None):
            qs = kwargs['brand']
            query = query.filter(Q(brand__name__icontains=qs) | Q(brand__name__iexact=qs)).distinct()

        if kwargs.get('category', None):
            qs = kwargs['category']
            query = query.filter(Q(category__name__icontains=qs) | Q(category__name__iexact=qs)).distinct()

        if kwargs.get('type_of_product', None):
            qs = kwargs['type_of_product']
            query = query.filer(Q(type__name__icontains=qs) | Q(type__name__iexact=qs)).distinc()

        if kwargs.get('business_card', None):
            qs = kwargs['business_card']
            query = query.filer(Q(card__name__icontains=qs) | Q(card__name__iexact=qs)).distinct()

        if kwargs.get('sort_by', None):
            qs = kwargs['sort_by']
            is_asc = kwargs.get('is_asc', False)
            if not is_asc:
                qs = f"-{qs}"
            query = query.order_by(qs)

        if kwargs.get('min_rating', None):
            qs = kwargs['min_rating']
            query = query.filter(Q(sub_product__avg_rating__qt=qs) | Q(sub_product__avg_rating__iexact=qs)).distinct()

        if kwargs.get('max_price', None):
            qs = kwargs['max_rating']
            query = query.filter(Q(sub_product__avg_rating__lt=qs) | Q(sub_product__avg_rating=qs)).distinct()

        return query

    product = graphene.Field(
        ProductType,
        id=graphene.ID(required=True),
        description='Response data about existing product.'
    )

    @staticmethod
    def resolve_product(cls, info, id):
        query = Product.objects.select_related('card', 'type').prefetch_related(
            'brand', 'category', 'sub_product', 'sub_product__attributes',
            'sub_product__comments', 'sub_product__stock'
        ).get(id=id)

        return query


schema = graphene.Schema(query=Query, mutation=Mutation)
