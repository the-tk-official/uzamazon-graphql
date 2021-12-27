from django.utils.translation import gettext_lazy as _

from .models import Brand, Category, Type


class ProductData:
    """
    Returns data to link from many to many fields.
    """

    @staticmethod
    def get_brands(product_data):
        brands = []
        for product_brand in product_data:
            try:
                brand = Brand.objects.get(pk=product_brand.id)
            except Brand.DoesNotExist:
                raise Exception(_("Enter an existing brands!"))
            brands.append(brand)
        return brands

    @staticmethod
    def get_categories(product_data):
        categories = []
        for product_category in product_data:
            try:
                category = Category.objects.get(pk=product_category.id)
            except Category.DoesNotExist:
                raise Exception(_("Enter an existing categories!"))
            categories.append(category)
        return categories

    @staticmethod
    def get_type(product_data):
        try:
            product_type = Type.objects.get(id=product_data.id)
        except Type.DoesNotExist:
            raise Exception(_("Enter an existing type of product!"))
        return product_type
