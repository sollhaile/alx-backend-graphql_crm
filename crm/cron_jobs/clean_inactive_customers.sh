#!/bin/bash

timestamp=$(date "+%Y-%m-%d %H:%M:%S")
deleted_count=$(python3 alx-backend-graphql_crm/manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(order__isnull=True, created__lt=cutoff).delete()
print(deleted)
")
echo \"$timestamp - Deleted $deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
