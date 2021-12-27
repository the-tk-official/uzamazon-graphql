import graphene


class BusinessCardInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    site = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    instagram = graphene.String(required=True)


class BrandInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class TypeInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    gender = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)


class SubProductInput(graphene.InputObjectType):
    sku = graphene.String(required=True)
    discount = graphene.Float()
    retail_price = graphene.Decimal(required=True)
    sale_price = graphene.Decimal(required=True)
    store_price = graphene.Decimal(required=True)
    weight = graphene.Float(required=True)
    is_active = graphene.Boolean(required=True)


class StockInput(graphene.InputObjectType):
    last_checked = graphene.DateTime()
    units = graphene.Int()
    units_sold = graphene.Int()


class AttributeInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    value = graphene.String(required=True)


class CommentInput(graphene.InputObjectType):
    comment = graphene.String()
    rating = graphene.Int(required=True)
    is_active = graphene.Boolean()
