#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/../.." || exit 1

# Get the Python interpreter from the virtual environment
PYTHON=$(which python)

# Run cleanup and log result
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
deleted_count=$($PYTHON manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(orders__created_at__gte=cutoff).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

echo "[$timestamp] Deleted customers: $deleted_count" >> /tmp/customer_cleanup_log.txt
