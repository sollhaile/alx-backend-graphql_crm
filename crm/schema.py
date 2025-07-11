import graphene
from graphene import Field, List, String, Float, Int, ID, Mutation, InputObjectType
from graphene_django.types import DjangoObjectType
from .models import Customer, Product, Order
from django.utils import timezone
from graphene_django.filter import DjangoFilterConnectionField
from .filters import CustomerFilter, ProductFilter, OrderFilter
from .models import Customer, Product, Order
from graphene import ObjectType
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re

# GraphQL Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

# Input Types
class CustomerInput(InputObjectType):
    name = String(required=True)
    email = String(required=True)
    phone = String()

class ProductInput(InputObjectType):
    name = String(required=True)
    price = Float(required=True)
    stock = Int()

# Create Customer Mutation
class CreateCustomer(Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = Field(CustomerType)
    message = String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")
        if input.phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', input.phone):
            raise Exception("Invalid phone number format")
        customer = Customer.objects.create(
            name=input.name,
            email=input.email,
            phone=input.phone or ""
        )
        return CreateCustomer(customer=customer, message="Customer created successfully")

# Bulk Create Customers
class BulkCreateCustomers(Mutation):
    class Arguments:
        input = List(CustomerInput, required=True)

    customers = List(CustomerType)
    errors = List(String)

    def mutate(self, info, input):
        created = []
        errors = []
        for entry in input:
            try:
                if Customer.objects.filter(email=entry.email).exists():
                    raise Exception(f"Email {entry.email} already exists")
                if entry.phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', entry.phone):
                    raise Exception(f"Invalid phone number: {entry.phone}")
                created.append(Customer.objects.create(
                    name=entry.name,
                    email=entry.email,
                    phone=entry.phone or ""
                ))
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(customers=created, errors=errors)

# Create Product
class CreateProduct(Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be positive")
        if input.stock is not None and input.stock < 0:
            raise Exception("Stock cannot be negative")
        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=input.stock if input.stock is not None else 0
        )
        return CreateProduct(product=product)

# Create Order
class CreateOrder(Mutation):
    class Arguments:
        customer_id = ID(required=True)
        product_ids = List(ID, required=True)
        order_date = String()

    order = Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(id=customer_id)
            products = Product.objects.filter(id__in=product_ids)
            if not products:
                raise Exception("No valid products found")

            order = Order.objects.create(
                customer=customer,
                order_date=order_date or timezone.now(),
                total_amount=sum(p.price for p in products)
            )
            order.products.set(products)
            order.save()
            return CreateOrder(order=order)

        except ObjectDoesNotExist as e:
            raise Exception("Invalid customer or product ID")

# Query
class Query(graphene.ObjectType):
    customers = List(CustomerType)
    products = List(ProductType)
    orders = List(OrderType)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.select_related('customer').prefetch_related('products')

# Mutation
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
