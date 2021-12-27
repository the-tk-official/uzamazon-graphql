import graphene

from product.schema import schema as product_schema
from user.schema import schema as user_schema


class Query(product_schema.Query, user_schema.Query, graphene.ObjectType):
    pass


class Mutation(product_schema.Mutation, user_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
