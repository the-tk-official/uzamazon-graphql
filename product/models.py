from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class BusinessCard(models.Model):
    """
    Business card table
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='business_card'
    )
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('name of the store or company'),
        help_text=_(
            'format: required, max-128'
        )
    )
    site = models.URLField(
        max_length=128,
        unique=True,
        verbose_name=_('web-site'),
        help_text=_(
            'format: required, unique, max-128'
        )
    )
    phone_regex = RegexValidator(
        regex=r'\A\+998\d{2}\d{3}\d{2}\d{2}\Z',
        message='Phone number must be entered in the format: "+998 99 999 99 99". Up to the 12 digits allowed.'
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        unique=True,
        verbose_name=_('additional phone number'),
        help_text=_(
            'format: required, unique, max-13'
        )
    )
    instagram = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('instagram'),
        help_text=_(
            'format: required, unique, max-128'
        )
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('date business card created'),
        help_text=_('format: Y-m-d H:M:S'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date business card updated'),
        help_text=_('format: Y-m-d H:M:S')
    )

    class Meta:
        verbose_name = _('Business card')
        verbose_name_plural = _('Business cards')

    def __str__(self):
        return f'{self.user.email}  |  {self.name}'


class BusinessCardImage(models.Model):
    """
    Business Card's Image table
    """
    card = models.OneToOneField(
        BusinessCard,
        on_delete=models.CASCADE,
        related_name='image'
    )
    image = models.ImageField(
        upload_to="images/business_card/%Y/%m/%d/",
        verbose_name=_("business card image"),
        help_text=_('format: required')
    )
    alt_text = models.CharField(
        max_length=256,
        default=_("business card's image alternative text"),
        verbose_name=_('alternative text'),
        help_text=_('format: required')
    )

    class Meta:
        verbose_name = _('Business card image')
        verbose_name_plural = _('Business card images')

    def __str__(self):
        return f'{self.card.name}  |  {self.image}'


class Brand(models.Model):
    """
    Product brand table
    """

    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_('brand name'),
        help_text=_('format: required, unique, max-256'),
    )

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Category table
    """

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('category name'),
        help_text=_('format: required, max-128')
    )

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')

    def __str__(self):
        return self.name


class Type(models.Model):
    """
    Product type model
    """
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_('type of product'),
        help_text=_('format: required, unique, max-256')
    )

    class Meta:
        verbose_name = _('Product type')
        verbose_name_plural = _('Product types')

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product detail table
    """

    GENDER_CHOICES = (
        ('A', _('All')),
        ('M', _('Male')),
        ('F', _('Female'))
    )

    card = models.ForeignKey(
        BusinessCard,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(
        max_length=256,
        verbose_name=_('product name'),
        help_text=_('format: required, max-256')
    )
    description = models.TextField(
        verbose_name=_('product description'),
        help_text=_('format: required')
    )
    brand = models.ManyToManyField(Brand, related_name='product_brands')
    category = models.ManyToManyField(Category, related_name='product_categories')
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=1,
        help_text=_(
            'format: required'
        ),
        verbose_name=_("gender"),
    )
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='product_types')
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('product visibility'),
        help_text=_('format: true=product visible')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('date product created'),
        help_text=_('format: Y-m-d H:M:S'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date product last updated'),
        help_text=_('format: Y-m-d H:M:S')
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name


class SubProduct(models.Model):
    """
    Sub product table
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sub_product'
    )
    discount = models.FloatField(
        default=0,
        verbose_name=_('product discount'),
        help_text=_('format: required')
    )
    avg_rating = models.FloatField(
        default=0,
        verbose_name=_('average rating of sub-product')
    )
    number_of_comment = models.PositiveIntegerField(
        default=0,
        verbose_name=_('number of comment')
    )
    retail_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('recommended retail price'),
        help_text=_('format: maximum price 9.999.999,99'),
        error_messages={
            'name': {
                'max_length': _('the price must be between 0 and 9.999.999,99')
            }
        }
    )
    sale_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('sale price'),
        help_text=_('format: maximum price 9.999.999,99'),
        error_messages={
            'name': {
                'max_length': _('the price must be between 0 and 9.999.999,99')
            }
        }
    )
    sku = models.CharField(
        max_length=16,
        verbose_name=_('universal product code'),
        help_text=_('format: required, unique, max-16'),
    )
    store_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('regular store price'),
        help_text=_('format: maximum price 9.999.999,99'),
        error_messages={
            'name': {
                'max_length': _('the price must be between 0 and 9.999.999,99')
            }
        }
    )
    weight = models.FloatField(
        verbose_name=_('product weight'),
        help_text=_('format: required')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('product visibility'),
        help_text=_('format: true=product visible')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('data sub-product created'),
        help_text=_('format: Y-m-d H:M:S'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date sub-product updated'),
        help_text=_('format: Y-m-d H:M:S')
    )

    class Meta:
        verbose_name = _('Sub product')
        verbose_name_plural = _('Sub products')

    def __str__(self):
        return f'{self.product.name}  |  {self.sku}'


class SubProductImage(models.Model):
    """
    Sub-product's Image table
    """
    sub_product = models.ForeignKey(
        SubProduct,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(
        upload_to="images/sub_product/%Y/%m/%d/",
        verbose_name=_("sub-product image"),
        help_text=_('format: required')
    )
    alt_text = models.CharField(
        max_length=256,
        default=_("sub-product's image alternative text"),
        verbose_name=_('alternative text'),
        help_text=_('format: required')
    )

    class Meta:
        verbose_name = _('Business card image')
        verbose_name_plural = _('Business card images')

    def __str__(self):
        return f'{self.sub_product.sku}  |  {self.image}'


class Stock(models.Model):
    """
    The product stoke table
    """

    sub_product = models.OneToOneField(
        SubProduct,
        on_delete=models.CASCADE,
        related_name='stock'
    )
    last_checked = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('inventory stock check date'),
        help_text=_('format: Y-m-d H:M:S, null-true, blank-true')
    )
    units = models.IntegerField(
        default=0,
        verbose_name=_('units/qty of stock'),
        help_text=_('format: required, default-0')
    )
    units_sold = models.IntegerField(
        default=0,
        verbose_name=_('units sold to date'),
        help_text=_('format: required, default-0')
    )

    class Meta:
        verbose_name = _('stock')
        verbose_name_plural = _('stocks')

    def __str__(self):
        return f'{self.sub_product.sku}  |  {self.units}'


class Attribute(models.Model):
    """
    Product attribute table
    """

    sub_product = models.ForeignKey(SubProduct, on_delete=models.CASCADE, related_name="attributes")
    name = models.CharField(
        max_length=256,
        verbose_name=_('product attribute name'),
        help_text=_('format: required, unique, max-256')
    )
    description = models.TextField(
        verbose_name=_('product attribute description'),
        help_text=_('format: required')
    )
    value = models.CharField(
        max_length=256,
        verbose_name=_('attribute value'),
        help_text=_('format: required, max-256')
    )

    def __str__(self):
        return f'{self.sub_product.product.name}    |    {self.sub_product.sku}    |    {self.name}'

    class Meta:
        verbose_name = _('Product attributes')
        verbose_name_plural = _('Product attributes')
        unique_together = ('sub_product', 'name', 'value')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    sub_product = models.ForeignKey(SubProduct, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('comments')
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('rating'),
        help_text=_('format: min=1, max=5, required')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('comments visibility'),
        help_text=_('format: true=comment visible')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('data comment created'),
        help_text=_('format: Y-m-d H:M:S'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date comment updated'),
        help_text=_('format: Y-m-d H:M:S')
    )

    def __str__(self):
        return f'{self.user.email}    |    {self.sub_product.sku}   |   {self.rating}'

    class Meta:
        verbose_name = _('Sub product comment')
        verbose_name_plural = _('Sub product comments')
        unique_together = ('user', 'sub_product')

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)

        number_of_comment = 0
        sum_of_rating = 0
        sub_product = self.sub_product

        comments = Comment.objects.filter(sub_product=sub_product, is_active=True)
        for comment in comments:
            number_of_comment += 1
            sum_of_rating += comment.rating
        avg_rating = float(sum_of_rating / number_of_comment)

        SubProduct.objects.filter(id=sub_product.id).update(
            number_of_comment=number_of_comment, avg_rating=avg_rating
        )

    def delete(self, *args, **kwargs):

        number_of_comment = 0
        sum_of_rating = 0
        sub_product = self.sub_product

        super(Comment, self).delete(*args, **kwargs)

        comments = Comment.objects.filter(sub_product=sub_product, is_active=True)

        for comment in comments:
            number_of_comment += 1
            sum_of_rating += comment.rating

        if sum_of_rating != 0:
            avg_rating = float(sum_of_rating / number_of_comment)
        else:
            avg_rating = 0

        sub = SubProduct.objects.get(id=sub_product.id)
        sub.number_of_comment = number_of_comment
        sub.avg_rating = avg_rating
        sub.save()
