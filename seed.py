import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

Customer.objects.create(name="Test User", email="test@example.com")
Product.objects.create(name="Monitor", price=120.00, stock=5)
Product.objects.create(name="Keyboard", price=40.00, stock=10)

print("Seeded database!")
