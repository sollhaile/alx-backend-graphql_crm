import graphene
from graphene_django import DjangoObjectType
from .models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    success = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        # ✅ Queries products with stock < 10
        products = Product.objects.filter(stock__lt=10)
        updated = []

        for product in products:
            # ✅ Increments their stock by 10
            product.stock += 10
            product.save()
            updated.append(product)

        # ✅ Returns list of updated products and a success message
        return UpdateLowStockProducts(
            success=f"{len(updated)} products restocked.",
            updated_products=updated
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")

schema = graphene.Schema(query=Query, mutation=Mutation)
